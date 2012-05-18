
"""
SG-specific Form helpers
"""

from __future__ import absolute_import

import re
import time

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.core.validators import RegexValidator
from django.forms.fields import Field, Select
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode

# from http://www.ura.gov.sg/realEstateWeb/resources/misc/list_of_postal_districts.htm
postcode_re = re.compile(r'^(?!(83|84|85|86|87|88|89))([0-8][0-9])\d{4}$')
# RE for both NRIC and FIN.  Check sum and validity of the numerical part
# are not calculated, due to branching rules and b/c the checksum isn't
# in the public domain.
# Format : @0000000#
# @ is centry marker, S,T for NRIC, F,G for FIN
# 0000000 is the serial no, with aditional constraints for birth year.
# # is Checksum.
nric_re = re.compile(r'([sftg])\d{7}[a-z]$',re.IGNORECASE)
mobile_phone_re = re.compile(r'^[(]?(?P<cc>\+65)[)]?(?P<num>[89]\d{7})')
phone_re = re.compile(r'^[(]?(?P<cc>\+65)[)]?(?P<num>[3689]\d{7})')

class NRICValidator(RegexValidator):
    code = 'invalid'
    message = _('Enter a valid NRIC/FIN number')
    regex = nric_re

    def __call__(self,value):
        super(NRICValidator,self).__call__(value)

validate_nric = NRICValidator()

class SGPhoneValidator(RegexValidator):
    code = 'invalid'
    message = _('Enter a valid phone number'),
    regex = phone_re

    def __call__(self,value,mobile_phone_only=False):
        if mobile_phone_only:
            self.regex = mobile_phone_re
        super(SGPhoneValidator,self).__call__(value)

validate_SG_phone = SGPhoneValidator()

class SGPostCodeValidator(RegexValidator):
    code = 'invalid'
    message = _('Enter a valid post code'),
    regex = postcode_re

    def __call__(self,value):
        super(SGPostCodeValidator,self).__call__(value)

validate_SG_postcode = SGPostCodeValidator()

class SGPostCodeField(Field):
    """
    A Singaporian post code field.

    http://www.ura.gov.sg/realEstateWeb/resources/misc/list_of_postal_districts.htm
    """
    error_messages = {
            'invalid': _('Enter a valid post code'),
            'required': _('Post code is required'),
            }
    validators = [validate_SG_postcode]

    def to_python(self,value):
        return value.strip()

    def clean(self,value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value

class SGPhoneNumberField(Field):
    """
    Singaporian phone number field.

    http://en.wikipedia.org/wiki/Telephone_numbers_in_Singapore
    """
    default_error_messages = {
            'invalid': _('Enter a valid phone number'),
            }
    validators = [validate_SG_phone]

    def to_python(self,value):
        return value.strip()

    def clean(self,value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        v_search = phone_re.search(value)
        if not v_search:
            raise ValidationError(self.default_error_messages['invalid'])

        return u"{0}{1}".format(v_search.group('cc'),
                                v_search.group('num'))

class SGNationalRegistrationIdentityCard(Field):
    """
    Singaporian NRIC and FIN card

    http://http://en.wikipedia.org/wiki/National_Registration_Identity_Card
    """
    error_messages = {
            'invalid': _('Enter a valid NRIC/FIN number'),
            'required': _('NRIC/FIN is required'),
                }
    validators = [RegexValidator(nric_re,code='invalid')]

    def to_python(self,value):
        return value.strip()

    def validate(self, value):
        if value in EMPTY_VALUES and self.required:
            raise ValidationError(self.error_messages['required'])

    def clean(self,value):
        """Validates NRIC/FIN number, cleans, etc.
        raises ValidationError on any error"""
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value.upper()
