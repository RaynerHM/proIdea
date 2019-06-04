from projectIdeas.settings import PASS_LDAP, RUTA_LOG
from django.contrib.auth.models import User
import logging

logging.config.dictConfig({
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'console': {
			'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
		},
		'file': {
			'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
		}
	},
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'console'
		},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'formatter': 'file',
			'filename': RUTA_LOG
		}
	},
	'loggers': {
		'': {
			'level': 'DEBUG',
			'handlers': ['console', 'file']
		},
		'django.request': {
			'level': 'DEBUG',
			'handlers': ['console', 'file']
		}
	}
})

def run():
	try:
		users = User.objects.all().order_by('first_name')
		
		for user in users:
			user.set_password(PASS_LDAP)
			user.save()

	except Exception as ex:
		logger.error(ex)
