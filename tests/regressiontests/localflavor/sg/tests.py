import warnings

from django.contrib.localflavor.sg.forms import (SGPhoneNumberField,
        SGPostCodeField, SGNationalRegistrationIdentityCard)

from django.test import SimpleTestCase

class SGLocalFlavorTests(SimpleTestCase):
    """Test the form"""
    def test_phone(self):
        error_invalid = [u'Enter a valid phone number']
        valid = {
                '+6594761111':'+6594761111',
                '(+65)94761111':'+6594761111',
                '+6565521111':'+6565521111',
                }
        invalid = {
                '94761111':error_invalid,
                '(+65)44761111':error_invalid,
                '+6365521111':error_invalid,
                }
        self.assertFieldOutput(SGPhoneNumberField, valid, invalid)

    def test_mobile(self):
        error_invalid = [u'Enter a valid phone number']
        valid = {
                '+6594761111':'+6594761111',
                '(+65)94761111':'+6594761111',
                '+6585521111':'+6585521111',
        }
        invalid = {
                '94761111':error_invalid,
                '(+65)44761111':error_invalid,
                '+6365521111':error_invalid,
                '+6565521111':error_invalid,
                }
        self.assertFieldOutput(SGPhoneNumberField, valid, invalid,
                field_kwargs={'mobile_phone_only':True})

    def test_postcode(self):
        error_invalid = [u'Enter a valid post code']
        error_required = [u'Post code is required']
        valid = {
                '570248':'570248',
                '010001':'010001',
                '580222':'580222',
                }
        invalid = {
                '852222':error_invalid,
                'm5d-2g4':error_invalid,
                '123':error_invalid,
                '':error_required,
                }
        self.assertFieldOutput(SGPostCodeField, valid, invalid,
                field_kwargs={'required':True})

    def test_NRIC_num(self):
        error_invalid = [u'Enter a valid NRIC/FIN Number']
        valid = {
                'S0850356G':'S0850356G',
                'T0850356C':'T0850356C',
                'F8554629P':'F8554629P',
                'G0854629R':'G0854629R',
                'g0854629R':'G0854629R',
                }
        invalid= {
                'S0123F':error_invalid,
                'R0850356G':error_invalid,
                'F8554629PP':error_invalid,
                }
        self.assertFieldOutput(SGNationalRegistrationIdentityCard, valid, invalid)
