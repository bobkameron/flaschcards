from django.db import models
from datetime import timedelta 
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now


# Create your models here.


#from django.contrib.auth.models import AbstractUser


class Card (models.Model):
    
    # max length of any word or definition on the card 
    max_length = 255 
    
    '''
    seconds_per_minute = 60 
    minutes_per_hour = 60
    seconds_per_hour = seconds_per_minute  * minutes_per_hour 
    hours_per_day = 24
    seconds_per_day = seconds_per_minute  * minutes_per_hour * hours_per_day 
    days_per_month = 30.437 
    seconds_per_month = seconds_per_minute  * minutes_per_hour * hours_per_day * days_per_month 
    
    time_delta = [ 0 , 5 , 25, 2 * seconds_per_minute , 10 * seconds_per_minute, 1 * seconds_per_hour,
    5 * seconds_per_hour, 1 * seconds_per_day, 5 * seconds_per_day, 25 * seconds_per_day, 4 * seconds_per_month]
    '''
    time_delta = [
        timedelta(seconds = 0), 
        timedelta(seconds = 5), 
        timedelta(seconds = 25),
        timedelta(minutes = 2 ),
        timedelta(minutes = 10),
        timedelta(hours = 1),
        timedelta(hours = 5),
        timedelta(days= 1),
        timedelta(days = 5),
        timedelta(days = 25),
        relativedelta(months = +4),
         ]

    word  = models.CharField( max_length= max_length,  null = False, blank = False , unique = True  )

    definition = models.CharField( max_length= max_length,  null = False, blank = False  )

    datetime_to_next_appearance = models.DateTimeField (default = now , null = False )

    lowest_bin, highest_bin = 0, 11 

    max_incorrect = 10 

    # there must be constraint that  0 <= number_times_incorrect <= 10 
    number_times_incorrect = models.IntegerField ( default = 0 , null = False )

    # there must be constraint that 0 <= bin <= 11     11 means that card never gets reviewed again 
    bin = models.IntegerField ( default = lowest_bin, null = False )


    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_number_times_incorrect_range",
                check=models.Q(number_times_incorrect__range=(0, 10  )),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_bin_range",
                check=models.Q(bin__range=(0, 11)),
            ),
        ]