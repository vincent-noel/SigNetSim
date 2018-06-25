from signetsim.models import ComputationQueue, Optimization, Continuation
from django.conf import settings
from dill import loads, dumps
NB_CORES = settings.MAX_CORES

def add_computation(project, entry, object, timeout=None):

	if isinstance(entry, Optimization):
		entry.status = Optimization.QUEUED
		entry.save()
		comp = ComputationQueue(
			project=project,
			type=ComputationQueue.OPTIM,
			computation_id=entry.id,
			object=dumps(object).decode('Latin-1'),
			timeout=timeout
		)
		comp.save()

	elif isinstance(entry, Continuation):
		entry.status = Continuation.QUEUED
		entry.save()
		comp = ComputationQueue(
			project=project,
			type=ComputationQueue.CONT,
			computation_id=entry.id,
			object=dumps(object).decode('Latin-1'),
			timeout=timeout
		)
		comp.save()

	update_queue()

def get_next_computations(project=None):

	if project is None:
		return sorted(ComputationQueue.objects.all(), key=lambda comp: comp.id)

	else:
		return sorted(ComputationQueue.objects.filter(project=project), key=lambda comp: comp.id)


def get_nb_cores_running():

	optims = [comp for comp in Optimization.objects.all() if comp.status == Optimization.BUSY]

	nb_cores_optim = 0
	for optim in optims:
		nb_cores_optim += optim.cores

	nb_continuation = len([comp for comp in Continuation.objects.all() if comp.status == Continuation.BUSY])

	return nb_cores_optim + nb_continuation

def get_user_nb_cores_running(user):

	optims = [comp for comp in Optimization.objects.all() if comp.status == Optimization.BUSY and comp.project.user == user]

	nb_cores_optim = 0
	for optim in optims:
		nb_cores_optim += optim.cores

	nb_continuation = len([comp for comp in Continuation.objects.all() if comp.status == Continuation.BUSY and comp.project.user == user])

	return nb_cores_optim + nb_continuation

def can_execute_computation(next_computation):

	if next_computation is not None:
		if next_computation.type == ComputationQueue.OPTIM:
			optim = Optimization.objects.get(id=next_computation.computation_id)
			nb_cores = optim.cores
		else:
			nb_cores = 1

		user_quota = next_computation.project.user.max_cores
		enough_on_server = (NB_CORES - get_nb_cores_running()) >= nb_cores
		enough_for_user = (user_quota - get_user_nb_cores_running(next_computation.project.user)) >= nb_cores
		user_has_quota = next_computation.project.user.used_cpu_time < next_computation.project.user.max_cpu_time
		return enough_on_server and enough_for_user and user_has_quota
	else:
		return False

def optim_success(object, optim):

	if optim.isInterrupted():
		object.status = Optimization.INTERRUPTED
	else:
		object.status = Optimization.ENDED
	object.save()

	if optim.elapsedTime is not None:
		user = object.project.user
		user.used_cpu_time = user.used_cpu_time + optim.elapsedTime
		user.save()

	update_queue()

def optim_error(object, optim, error=None):

	if optim.isInterrupted():
		object.status = Optimization.INTERRUPTED
	else:
		object.status = Optimization.ERROR

	object.result = dumps(optim).decode('Latin-1')
	if error is not None:
		object.error = error
	object.save()

	if optim.elapsedTime is not None:
		user = object.project.user
		user.used_cpu_time = user.used_cpu_time + optim.elapsedTime
		user.save()

	update_queue()

def cont_success(object, cont, result):
	object.result = dumps(result).decode('Latin-1')
	object.status = Continuation.ENDED
	object.save()

	if cont.elapsedTime is not None:
		user = object.project.user
		user.used_cpu_time = user.used_cpu_time + cont.elapsedTime
		user.save()

	update_queue()

def cont_error(object, cont, error=None):
	object.status = Continuation.ERROR
	if error is not None:
		object.error = error
	object.save()

	if cont.elapsedTime is not None:
		user = object.project.user
		user.used_cpu_time = user.used_cpu_time + cont.elapsedTime
		user.save()

	update_queue()

def execute_computation(next_computation):

	if next_computation.type == ComputationQueue.OPTIM:
		optimization = Optimization.objects.get(id=next_computation.computation_id)
		optim = loads(next_computation.object.encode('Latin-1'))

		if not optim.isInterrupted():
			optim.run_async(
				success=lambda executed_optim: optim_success(optimization, executed_optim),
				failure=lambda executed_optim, error=None: optim_error(optimization, executed_optim, error),
				nb_procs=optimization.cores,
				timeout=next_computation.timeout
			)

		else:
			optim.restart_async(
				success=lambda executed_optim: optim_success(optimization, executed_optim),
				failure=lambda executed_optim, error=None: optim_error(optimization, executed_optim, error),
				nb_procs=optimization.cores,
				timeout=next_computation.timeout
			)
		optimization.status = Optimization.BUSY
		optimization.save()
		next_computation.delete()

	else:
		continuation = Continuation.objects.get(id=next_computation.computation_id)
		cont = loads(next_computation.object.encode('Latin-1'))
		cont.run_async(
			lambda res: cont_success(continuation, cont, res),
			lambda error=None: cont_error(continuation, cont, error)
		)
		continuation.status = Continuation.BUSY
		continuation.save()
		next_computation.delete()


def update_queue():

	for computation in get_next_computations():
		if can_execute_computation(computation):
			execute_computation(computation)

def updateComputationTime(user, time):

	user.used_cpu_time += time/3600
	user.save()