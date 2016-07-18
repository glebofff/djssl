from django.db import models
from OpenSSL import crypto


class Cert(models.Model):
    class Meta:
        db_table = 'certs'

    __aliases__ = {
        'c': 'C',
        'o': 'O',
        'cn': 'CN',
        'sn': 'surName',
        'ea': 'emailAddress'
    }

    c = models.CharField(max_length=3, null=True, db_index=True, verbose_name='Country')
    o = models.CharField(max_length=64, null=True, db_index=True, verbose_name='Organization')
    cn = models.CharField(max_length=64, null=True, db_index=True, verbose_name='Common Name')
    sn = models.CharField(max_length=40, null=True, db_index=True, verbose_name='SurName')
    ea = models.CharField(max_length=255, null=True, db_index=True, verbose_name='Email Address')
    filename = models.CharField(max_length=255, null=False, default='', db_index=True)
    body = models.TextField(null=True)

    def frombuffer(self, buf):
        try:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, buf)
            subj = dict(cert.get_subject().get_components())
            for field, alias in Cert.__aliases__.iteritems():
                setattr(self, field, subj.get(alias))
            self.body = buf
            return True

        except crypto.Error as e:
            raise e

    def verbose_dict(self):
        res = {}
        for f in self._meta.concrete_fields:
            if f.name not in self.__aliases__.iterkeys():
                continue
            if f.verbose_name:
                res[f.verbose_name] = f.value_from_object(self)
        return res
