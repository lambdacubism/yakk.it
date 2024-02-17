
from django.db import models
# from django.core.validators import int_list_validator

def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )

class topics( models.Model ):
    TopicNr				    = models.IntegerField(  default=0 )
    TopicText			    = models.CharField(     max_length=77 )
    TopicChosenCategory     = models.IntegerField(  default=1 )
    TopicCreatedBy          = models.IntegerField(  default=0 )
    TopicCreatedOnAt        = models.DateTimeField( auto_now_add=True )
    TopicStatus			    = models.IntegerField(  default=0 )             # int : 0 blank, 1 governed, 2 sensitized, 3 commodified, 4 business
    TopicGeneration		    = models.IntegerField(  default=0 )             # int : 0 genesis, 1 …, 2 …, A…, B…, 	(smart contract)
    TopicAuctionTiming	    = models.IntegerField(  default=0 )             # int : 0 blank, 1 auction started, 2 auction ended
    TopicAuctionStartedOnAt	= models.DateTimeField( auto_now_add=True )
    TopicAuctionEndedOnAt	= models.DateTimeField( auto_now_add=True )

class yakks( models.Model ):
    # Web3Set1
    YakkNr              = models.IntegerField(  default=0 )
    Yakk                = models.CharField(     max_length=7777 )
    YakkChosenCategory  = models.IntegerField(  default=1 )
    YakkTopicNr         = models.IntegerField(  null=False )
    YakkedBy            = models.IntegerField(  default=0 )
    YakkedOnAt          = models.DateTimeField( auto_now_add=True )
    YakkStatus          = models.IntegerField(  default=0 )
    YakkLanguage        = models.IntegerField(  default=1 )
    YakkNet             = models.IntegerField(  default=0 )
    YakkGeneration      = models.IntegerField(  default=0 )
    # Web3Set2
    YakkQtyOfLikes		= models.IntegerField(  default=0 )
    YakkQtyOfDislikes	= models.IntegerField(  default=0 )
    YakkQtyOfStrikes	= models.IntegerField(  default=0 )
    # Web2 only
    YakkW2Continuation  = models.IntegerField(  default=0 )
    YakkW2QtyOfRefsIn   = models.CharField( max_length=200 )    # validators=int_list_validator, max_length= 20 )   # int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)[source]
    YakkW2QtyOfRefsOut  = models.CharField( max_length=200 )    # validators=int_list_validator, max_length= 20 )   # int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)[source]

class accounts( models.Model ):
    AccountNr			    = models.IntegerField(  default=0 )
    AccountStatus		    = models.IntegerField(  default=0 )
    AccountWalletID		    = models.CharField(     max_length=32 )
    AccountNickname		    = models.CharField(     max_length=32 )
    AccountCreatedOnAt	    = models.DateTimeField( auto_now_add=True )
    AccountLiveliness	    = models.CharField( max_length=100 )    # validators=int_list_validator, max_length= 20 )   # int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)[source]int array (5 last entry)
    AccountGPA			    = models.IntegerField(  default=0 )
    AccountQtyOfYakks	    = models.CharField( max_length=100 )
    AccountQtyOfTopics	    = models.CharField( max_length=100 )
    AccountQtyOfLikes	    = models.IntegerField(  default=0 )
    AccountQtyOfDislikes    = models.IntegerField(  default=0 )
    AccounQtyOfStrikes	    = models.IntegerField(  default=0 )
    AccountOwnedTopics	    = models.CharField( max_length=5000 )    # validators=int_list_validator, max_length= 20 )   # int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)[source]int array (5 last entry)
    AccountAuctions	        = models.CharField( max_length=5000 )    # validators=int_list_validator, max_length= 20 )   # int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)[source]int array (5 last entry)
