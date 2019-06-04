from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import Idea, Categorie, Votes_Realized
from django.contrib.auth.models import User

from django.core.serializers import serialize
from django.contrib import auth
from datetime import datetime
from django.contrib.auth.decorators import permission_required, login_required
from projectIdeas.settings import RUTA_LOG
import json
import logging
import ldap
from projectIdeas.settings import AD_LDAP_URL, DOMAIN, PASS_LDAP

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


def login(request):
	logger = logging.getLogger('Inicio de Sesion')
	message = ''
	if request.method == 'POST':
		_user = request.POST.get('username')
		_password = request.POST.get('password')

		try:
			l = ldap.initialize(AD_LDAP_URL)
			l.protocol_version = ldap.VERSION3
			l.simple_bind_s("%s@%s" % (_user, DOMAIN), _password)
			l.unbind_s()
			user_auth = auth.authenticate(username=_user, password=PASS_LDAP)
			auth.login(request, user_auth)
			logger.info('%s inicio sesion correctamente.' %_user)
			return redirect(index)

		except ldap.INVALID_CREDENTIALS:
				message = 'Usuario o clave incorrecto'
				logger.warning(message)
		except ldap.SERVER_DOWN:
				message = 'No se pudo conectar con el servidor LDAP'
				logger.error(message)
		except Exception as ex:
			logger.warning(ex)
			message = 'Usuario o clave incorrecto'

	return render(request, 'login.html', {'message': message})


@login_required(login_url='/login')
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def index(request):
	logger = logging.getLogger('Index')

	data = {
		'user': '',
		'quantity': '',
		'ideas': [],
	}

	if request.method == 'POST':
		description = request.POST.get('description')
		category_hide = request.POST.get('category_hide')
		category = request.POST.get('category')
		anonimus = request.POST.get('anonimus')
		unique_name_category = 0

		try:
			if anonimus == 'on':
				anonimus = True
			else:
				anonimus = False

			if category_hide:
				category = Categorie.objects.get(pk=category_hide)
			else:
				category = Categorie.objects.create(
					name=category,
					unique_name=category
					.lstrip().rstrip().replace(' ', '_').lower()
				)

			unique_name_category = category

			Idea.objects.create(
				description=description,
				category=unique_name_category,
				anonimus=anonimus,
				author_id=request.user.id,
				publication_date=datetime.now(),
				quantity_positive_votes=0,
				quantity_negative_votes=0,
			)

		except Exception as ex:
			logger.error(ex)

		return redirect(index)

	elif request.method == 'GET':
		status = request.GET.get('status')
		try:
			if status == 'approved':
				ideas_query = Idea.objects.filter(approved=True).order_by('-id')
			elif status == 'discarded':
				ideas_query = Idea.objects.filter(discarded=True).order_by('-id')
			else:
				ideas_query = Idea.objects.all().order_by('-id')

			ideas = []
			for idea in ideas_query:
				vote = Votes_Realized.objects.filter(
					id_idea=idea.id, id_user=request.user.id).first()
				ideas.append(
					{
						'idea': idea,
						'vote': vote
					}
				)
			data['ideas'] = ideas
			data['quantity'] = len(ideas)

		except Exception as ex:
			logger.error(ex)
			message = ex

	data['user'] = request.user.get_full_name()
	return render(request, 'index.html', data)


@permission_required('appIdeas.can_validate_idea', raise_exception=True)
def validate_rrhh(request):
	logger = logging.getLogger('validate_rrhh')

	message = ''
	status = ''
	data = {
		'user': '',
		'quantity': '',
		'ideas': [],
	}

	if request.method == 'POST':
		decition = request.POST.get('decition')
		status_discarded = request.POST.get('status_discarded')
		status_approved = request.POST.get('status_approved')
		id_idea = request.POST.get('id_idea')

		try:
			if status_approved == 'True' and status_discarded == 'False':
				status = 'approved'
				message = 'Idea aprobada!'
			elif status_approved == 'False' and status_discarded == 'True':
				status = 'discarded'
				message = 'Idea descartada!'

			validate = Idea.objects.get(id=id_idea)
			validate.approved = status_approved
			validate.discarded = status_discarded
			validate.save()

		except Exception as ex:
			logger.error(ex)
			message = ex

		return HttpResponse(
			json.dumps({
				'message': message,
				'status': status,
			}), content_type="application/json"
		)

	elif request.method == 'GET':
		status = request.GET.get('status')
		try:
			if status == 'approved':
    				ideas_query = Idea.objects.filter(approved=True).order_by('-id')
			elif status == 'discarded':
				ideas_query = Idea.objects.filter(discarded=True).order_by('-id')
			else:
				ideas_query = Idea.objects.all().order_by('-id')

			ideas = []
			a = 0
			for idea in ideas_query:
				vote = Votes_Realized.objects.filter(
					id_idea=idea.id, id_user=request.user.id).first()
				ideas.append(
					{
						'idea': idea,
						'vote': vote
					}
				)

			data['ideas'] = ideas
			data['quantity'] = len(ideas_query)

		except Exception as ex:
			logger.error(ex)
			message = ex

	data['user'] = request.user.get_full_name()
	return render(request, 'validate_rrhh.html', data)


# ***********************************************************************#
# <-------------------------- Functions AJAX --------------------------> #
# ***********************************************************************#
def validation(data_args):
	_idea = data_args['idea']
	vote = data_args['vote']
	type_vote = data_args['type_vote']
	_id_user = data_args['id_user']
	like = 0
	dont_like = 0

	if type_vote == 'negative':
		type_antonym = 'positive'
	elif type_vote == 'positive':
		type_antonym = 'negative'

	try:
		my_vote = Votes_Realized.objects.filter(
			id_user=_id_user, id_idea=_idea.id, type=type_antonym).first()
	except Votes_Realized.DoesNotExist:
		my_vote = None

	if type_vote == 'positive':
		if _idea.quantity_negative_votes <= 0:
			dont_like = 0
		else:
			if my_vote:
				dont_like = (int(_idea.quantity_negative_votes) - 1)
			else:
				dont_like = (int(_idea.quantity_negative_votes))
		like = (int(_idea.quantity_positive_votes) + 1)

	elif type_vote == 'negative':
		if _idea.quantity_positive_votes <= 0:
			like = 0
		else:
			if my_vote:
				like = (int(_idea.quantity_positive_votes) - 1)
			else:
				like = (int(_idea.quantity_positive_votes))
		dont_like = (int(_idea.quantity_negative_votes) + 1)

	_idea.quantity_positive_votes = like
	_idea.quantity_negative_votes = dont_like

	vote.save()
	_idea.save()

	quantity = {
		'like': like,
		'dont_like': dont_like,
	}
	return quantity


@login_required(login_url='/login')
def votes_ajax(request):
	logger = logging.getLogger('votes_ajax')
	like = 0
	dont_like = 0
	vote = None
	quantity = {
		'like': 0,
		'dont_like': 0,
		'message': '',
	}
	data_args = {}

	if request.method == 'POST':
		type_vote = request.POST.get('type_vote')
		id_idea = request.POST.get('id_idea')
		_idea = Idea.objects.get(id=id_idea)
		id_user = request.user.id

		try:
			vote = Votes_Realized.objects.get(
				id_user=id_user, id_idea=_idea)
			vote.type = type_vote

			data_args['idea'] = _idea
			data_args['vote'] = vote
			data_args['type_vote'] = type_vote
			data_args['id_user'] = id_user

			quantity = validation(data_args)

		except Votes_Realized.DoesNotExist:
			users = User.objects.get(id=request.user.id)
			vote = Votes_Realized.objects.create(
				id_user=users,
				id_idea=_idea,
				type=type_vote
			)

			data_args['idea'] = _idea
			data_args['vote'] = vote
			data_args['type_vote'] = type_vote
			data_args['id_user'] = id_user

			quantity = validation(data_args)

		except Exception as ex:
			logger.error(ex)
			quantity['message'] = ('Error: %s ' % ex)

	return HttpResponse(
		json.dumps(quantity),
		content_type="application/json"
	)


def charge_category_ajax(request):
	category = Categorie.objects.all()
	categorie = {}
	unique_name_category = {}

	for category in category:
		categorie[category.name] = ''
		unique_name_category[category.name] = category.unique_name

	return HttpResponse(
		json.dumps({
			'categorie': categorie,
			'unique_name_category': unique_name_category,
		}),
		content_type="application/json"
	)


def auto_charge_ideas_ajax(request):
	logger = logging.getLogger('validate_rrhh')
	param = request.GET.get('params')
	ideas_query = None
	data = None

	try:
		if param:
			if param.split('=')[1] == 'approved':
				ideas_query = Idea.objects.filter(approved=True).order_by('-id')
			elif param.split('=')[1] == 'discarded':
				ideas_query = Idea.objects.filter(discarded=True).order_by('-id')
			else:
				ideas_query = Idea.objects.all().order_by('-id')
		else:
			ideas_query = Idea.objects.all().order_by('-id')

		data = serialize('json', ideas_query,
			use_natural_foreign_keys=True, use_natural_primary_keys=True
		)

	except Exception as ex:
		logger.error(ex)

	return HttpResponse(data, content_type='application/json')

