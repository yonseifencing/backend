from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_symbols,validate_no_special_characters
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from datetime import date
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,UserManager)



from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# 여기다가 쓰고 그냥 다른 html에 연결 하면 될 듯 ?
class User(AbstractBaseUser):
    name = models.CharField(
        max_length=10,
        
        validators=[validate_no_special_characters],
        error_messages={'unique':'이미 등록된 이름입니다'}
    )  # 이름
    user_pic = models.ImageField(default='default_profile_pic.jpg', upload_to='user_pics')
    # 유저 사진인데 이건 유저 페이지에서 수정버튼 누르면 될 듯 
    student_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique':'이미 등록된 학번입니다'}
    ) # 학번 
    major = models.CharField(
        max_length=20,
        
        validators=[validate_no_special_characters],
    
        
    ) # 학과
    current_year = date.today().year
    YEAR_CHOICES = [(str(year) + '-' + str(semester), str(year) + '-' + str(semester)) for year in range(1987, current_year) for semester in [1, 2]]
    join_year = models.CharField(
        max_length=7,
        choices=YEAR_CHOICES,
        default='2020-1', ) 
     # 입부년도 
    awards = models.CharField(
        max_length=9,
    )
    email = models.EmailField(max_length=254,verbose_name='email', unique=True)
    is_active = models.BooleanField(default =True)

    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD ='email'
    
    def __str__(self):
        return self.email # 이거 아마 이메일로 매칭이 되는것일껄?
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

   
class attendance(models.Model): # 출석 부분 
    attendant = models.ForeignKey(User, on_delete=models.CASCADE,related_name='attendants')



