from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from EntrepriseApp.models import Entreprise, Utilisateur
from ExpeditionsApp.models import Expedition
from OffersApp.models import Offres
from VehiculesApp.models import Vehicules

CAPACITY_RANGES = {
    "camionnette": (100, 1500),
    "fourgon": (1501, 3500),
    "camion_porteur": (3500, 19000),
    "semi_remorque": (19000, 26000),
}
VEHICLE_TYPES = tuple(CAPACITY_RANGES)


class Command(BaseCommand):
    help = "Create a large, valid and repeatable Faker dataset for local development."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="ChangeMe123!")
        parser.add_argument("--companies", type=int, default=20)
        parser.add_argument("--vehicles-per-transporter", type=int, default=4)
        parser.add_argument("--expeditions", type=int, default=40)
        parser.add_argument("--offers-per-expedition", type=int, default=3)
        parser.add_argument("--locale", default="fr_FR")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["companies"] < 2:
            raise ValueError("--companies must be at least 2")
        fake = Faker(options["locale"])
        Faker.seed(20261022)
        fake.seed_instance(20261022)

        companies = self._companies(fake, options["companies"], options["password"])
        transporters = [c for c in companies if c.type_entreprise == "transporteur"]
        chargeurs = [c for c in companies if c.type_entreprise == "chargeur"]
        vehicles = self._vehicles(
            transporters, options["vehicles_per_transporter"], fake
        )
        expeditions = self._expeditions(chargeurs, options["expeditions"], fake)
        offers = self._offers(
            expeditions,
            transporters,
            vehicles,
            options["offers_per_expedition"],
            fake,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed data ready: {len(companies)} companies, "
                f"{len(companies)} users, {len(vehicles)} vehicles, "
                f"{len(expeditions)} expeditions and {offers} offers."
            )
        )

    @staticmethod
    def _user(email, username, role, telephone, password):
        user = Utilisateur.objects.filter(email=email).first()
        if user is None:
            user = Utilisateur(email=email)
        user.username = username
        user.role = role
        user.telephone = telephone
        user.set_password(password)
        user.save()
        return user

    def _companies(self, fake, count, password):
        companies = []
        for index in range(count):
            role = "transporteur" if index % 2 else "chargeur"
            manager = self._user(
                email=f"seed.manager.{index:03d}@gmail.com",
                username=f"seed_manager_{index:03d}",
                role=role,
                telephone=f"2{index:07d}",
                password=password,
            )
            fiscal_number = (
                f"{index + 1000000:07d}A{'B' if index % 2 else 'D'}M{index + 1:03d}"
            )
            company, _ = Entreprise.objects.update_or_create(
                matricule_fiscal=fiscal_number,
                defaults={
                    "raison_social": f"{fake.company()} {index + 1}",
                    "type_entreprise": role,
                    "addresse": fake.address()[:255],
                    "gerant": manager,
                },
            )
            companies.append(company)
        return companies

    @staticmethod
    def _vehicles(transporters, per_company, fake):
        vehicles = []
        for company_index, company in enumerate(transporters):
            for vehicle_index in range(per_company):
                vehicle_type = VEHICLE_TYPES[vehicle_index % len(VEHICLE_TYPES)]
                minimum, maximum = CAPACITY_RANGES[vehicle_type]
                vehicle, _ = Vehicules.objects.update_or_create(
                    immatriculation=f"FAKE-{company_index:02d}-{vehicle_index:02d}",
                    defaults={
                        "capacite_kg": fake.random_int(minimum, maximum),
                        "type_vehicules": vehicle_type,
                        "disponible": True,
                        "entreprise": company,
                    },
                )
                vehicle.full_clean()
                vehicles.append(vehicle)
        return vehicles

    @staticmethod
    def _expeditions(chargeurs, count, fake):
        expeditions = []
        for index in range(count):
            vehicle_type = VEHICLE_TYPES[index % len(VEHICLE_TYPES)]
            minimum, maximum = CAPACITY_RANGES[vehicle_type]
            maximum = min(maximum, minimum + 500)
            expedition, _ = Expedition.objects.update_or_create(
                reference=f"EXP-FAKE-{index + 1:05d}",
                defaults={
                    "ville_depart": fake.city()[:67],
                    "ville_arrive": fake.city()[:67],
                    "poids_kg": Decimal(fake.random_int(minimum, maximum)),
                    "date_souhaitte": timezone.localdate(),
                    "description": fake.paragraph(nb_sentences=2),
                    "statut": "attribuée",
                    "entreprise": chargeurs[index % len(chargeurs)],
                },
            )
            expeditions.append(expedition)
        return expeditions

    @staticmethod
    def _offers(expeditions, transporters, vehicles, per_expedition, fake):
        offers = 0
        for expedition in expeditions:
            compatible = [
                vehicle
                for vehicle in vehicles
                if vehicle.capacite_kg >= expedition.poids_kg
                and CAPACITY_RANGES[vehicle.type_vehicules][0]
                <= expedition.poids_kg
                <= CAPACITY_RANGES[vehicle.type_vehicules][1]
            ]
            if not compatible:
                continue
            one_vehicle_per_company = {}
            for vehicle in compatible:
                one_vehicle_per_company.setdefault(vehicle.entreprise_id, vehicle)
            selected = list(one_vehicle_per_company.values())[:per_expedition]
            for vehicle in selected:
                offer = Offres.objects.filter(
                    expedition=expedition,
                    entreprise=vehicle.entreprise,
                    vehicule=vehicle,
                ).first()
                if offer is None:
                    offer = Offres(
                        expedition=expedition,
                        entreprise=vehicle.entreprise,
                        vehicule=vehicle,
                    )
                offer.prix = Decimal(fake.random_int(150, 950))
                offer.delai_jours = fake.random_int(1, 14)
                offer.statut = "proposee"
                offer.save()
                offers += 1
        return offers
