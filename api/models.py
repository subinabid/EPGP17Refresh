"""Models for the API app"""

from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore

STATES = (
    ("AP", "Andhra Pradesh"),
    ("AR", "Arunachal Pradesh"),
    ("AS", "Assam"),
    ("BR", "Bihar"),
    ("CG", "Chhattisgarh"),
    ("DL", "Delhi"),
    ("GA", "Goa"),
    ("GJ", "Gujarat"),
    ("HR", "Haryana"),
    ("HP", "Himachal Pradesh"),
    ("JK", "Jammu and Kashmir"),
    ("JH", "Jharkhand"),
    ("KA", "Karnataka"),
    ("KL", "Kerala"),
    ("MP", "Madhya Pradesh"),
    ("MH", "Maharashtra"),
    ("MN", "Manipur"),
    ("ML", "Meghalaya"),
    ("MZ", "Mizoram"),
    ("NL", "Nagaland"),
    ("OD", "Odisha"),
    ("PB", "Punjab"),
    ("RJ", "Rajasthan"),
    ("SK", "Sikkim"),
    ("TN", "Tamil Nadu"),
    ("TG", "Telangana"),
    ("TR", "Tripura"),
    ("UP", "Uttar Pradesh"),
    ("UK", "Uttarakhand"),
    ("WB", "West Bengal"),
    ("AN", "Andaman and Nicobar Islands"),
    ("CH", "Chandigarh"),
    ("DN", "Dadra and Nagar Haveli"),
    ("DD", "Daman and Diu"),
    ("LD", "Lakshadweep"),
    ("PY", "Puducherry"),
)

STUDY_CENTER_STATES = (
    ("BR", "Bihar"),
    ("CG", "Chhattisgarh"),
    ("CH", "Chandigarh"),
    ("DL", "Delhi"),
    ("GA", "Goa"),
    ("GJ", "Gujarat"),
    ("HR", "Haryana"),
    ("JH", "Jharkhand"),
    ("KA", "Karnataka"),
    ("KL", "Kerala"),
    ("MH", "Maharashtra"),
    ("MP", "Madhya Pradesh"),
    ("OD", "Odisha"),
    ("PB", "Punjab"),
    ("RJ", "Rajasthan"),
    ("TG", "Telangana"),
    ("TN", "Tamil Nadu"),
    ("UK", "Uttarakhand"),
    ("UP", "Uttar Pradesh"),
    ("WB", "West Bengal"),
)

STUDY_CENTER_CITIES = {
    "BR": ("Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia"),
    "CG": ("Raipur", "Bhilai", "Bilaspur", "Korba", "Durg"),
    "CH": ("Chandigarh", "CH"),
    "DL": ("New Delhi", "Delhi"),
    "GA": ("Panaji", "Vasco da Gama", "Margao", "Mapusa", "Ponda"),
    "GJ": ("Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"),
    "HR": ("Faridabad", "Gurugram", "Panipat", "Ambala", "Yamunanagar"),
    "JH": ("Ranchi", "Jamshedpur", "Dhanbad", "Bokaro Steel City", "Deoghar"),
    "KA": ("Bengaluru", "Mangaluru"),
    "KL": ("Thiruvananthapuram", "Kochi", "Kozhikode"),
    "MH": ("Mumbai", "Pune", "Nagpur", "Thane", "Nashik"),
    "MP": ("Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain"),
    "OD": ("Bhubaneswar", "Cuttack", "Rourkela", "Sambalpur", "Puri"),
    "PB": ("Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"),
    "RJ": ("Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer"),
    "TG": ("Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Ramagundam"),
    "TN": ("Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"),
    "UK": ("Dehradun", "Haridwar", "Roorkee", "Haldwani", "Kashipur"),
    "UP": ("Lucknow", "Kanpur", "Ghaziabad", "Agra", "Meerut"),
    "WB": ("Kolkata", "Asansol", "Siliguri", "Durgapur", "Bardhaman"),
}

GROUPS = (
    ("A", "Group A"),
    ("B", "Group B"),
    ("C", "Group C"),
    ("D", "Group D"),
    ("E", "Group E"),
    ("F", "Group F"),
)


class BatchInfo(models.Model):
    """Basic Information model"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="batch_info"
    )
    epgp_batch = models.IntegerField(
        null=False, blank=True, default=17, verbose_name="EPGP Batch"
    )
    epgp_group = models.CharField(
        max_length=1, null=False, blank=True, choices=GROUPS, default="A"
    )
    roll_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Roll Number (eg 75)"
    )
    homeState = models.CharField(max_length=100, null=True, blank=True, choices=STATES)
    homeTown = models.CharField(max_length=100, null=True, blank=True)
    currentCity = models.CharField(max_length=100, null=True, blank=True)
    studyCenterState = models.CharField(
        max_length=100, choices=STUDY_CENTER_STATES, default="KL"
    )
    studyCenterCity = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=[
            (city, city)
            for state_cities in STUDY_CENTER_CITIES.values()
            for city in state_cities
        ],
    )
    studyCenterName = models.CharField(max_length=100, null=True, blank=True)


class SocialLinks(models.Model):
    """Social Links model"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="social_links"
    )
    personalEmail = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    whatsapp = models.CharField(max_length=10, null=True, blank=True)
    telegram = models.CharField(max_length=10, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    other = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


class Employment(models.Model):
    """Employer model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.CharField(max_length=200)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.employer}"


SALUTATIONS = (
    ("Dr.", "Dr."),
    ("Prof.", "Prof."),
    ("Mr.", "Mr."),
    ("Ms.", "Ms."),
    ("Mrs.", "Mrs."),
)

AREAS = (
    ("FAC", "Finance, Accounting, and Control"),
    ("MM", "Marketing Management"),
    ("HLAM", "Humanities, Leadership, and Advanced Management"),
    ("OM", "Operations Management"),
    ("STR", "Strategy"),
    ("IS", "Information Systems"),
    ("ECON", "Economics"),
)


class Professor(models.Model):
    """Professor model"""

    salutation = models.CharField(
        max_length=10, choices=SALUTATIONS, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=50, choices=AREAS, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class Elective(models.Model):
    """Elective courses"""

    area = models.CharField(max_length=100, choices=AREAS, null=True, blank=True)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True, blank=True
    )
    credits = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class ElectiveOffering(models.Model):
    """Elective offerings for a batch"""

    epgp_batch = models.IntegerField(null=False, blank=True)
    term = models.IntegerField(null=False, blank=True)
    course = models.ForeignKey(
        Elective, on_delete=models.CASCADE, related_name="elective_offerings"
    )
    track = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True, default="")

    def __str__(self):
        return f"Batch {self.epgp_batch} - {self.course} - Q{self.term} - Track {self.track} - Section {self.section}"


class ElectiveEnrollment(models.Model):
    """Elective enrollment for users"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    elective_offering = models.ForeignKey(ElectiveOffering, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.elective_offering}"
