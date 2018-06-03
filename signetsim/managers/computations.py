from signetsim.models import ComputationQueue, Optimization, Continuation
from dill import loads, dumps
NB_CORES = 3

def list_computations(project=None):

	if project is None:
		return ComputationQueue.objects.all()

	else:
		return ComputationQueue.objects.filter(project=project)

def add_computation(project, entry, object):

	if isinstance(entry, Optimization):
		comp = ComputationQueue(project=project, type=ComputationQueue.OPTIM, computation_id=entry.id, object=dumps(object).decode('Latin-1'))
		comp.save()

	elif isinstance(entry, Continuation):
		comp = ComputationQueue(project=project, type=ComputationQueue.CONT, computation_id=entry.id, object=dumps(object).decode('Latin-1'))
		comp.save()

	update_queue()

def get_next_computation():

	ids = sorted([comp.id for comp in list_computations()])
	if len(ids) > 0:
		comp = ComputationQueue.objects.get(id=ids[0])
		return comp

def get_nb_cores_running():

	optims = [comp for comp in Optimization.objects.all() if comp.status == "BU"]

	nb_cores_optim = 0
	for optim in optims:
		nb_cores_optim += optim.cores

	nb_continuation = len([comp for comp in Continuation.objects.all() if comp.status == "BU"])

	return nb_cores_optim + nb_continuation

def get_user_nb_cores_running(user):

	optims = [comp for comp in Optimization.objects.all() if comp.status == "BU" and comp.project.user == user]

	nb_cores_optim = 0
	for optim in optims:
		nb_cores_optim += optim.cores

	nb_continuation = len([comp for comp in Continuation.objects.all() if comp.status == "BU" and comp.project.user == user])

	return nb_cores_optim + nb_continuation


def can_execute_next_computation():

	next_computation = get_next_computation()

	if next_computation is not None:
		if next_computation.type == ComputationQueue.OPTIM:
			optim = Optimization.objects.get(id=next_computation.computation_id)
			nb_cores = optim.cores
		else:
			nb_cores = 1

		user_quota = next_computation.project.user.max_cores
		enough_on_server = (NB_CORES - get_nb_cores_running()) >= nb_cores
		enough_for_user = (user_quota - get_user_nb_cores_running(next_computation.project.user)) >= nb_cores
		print("%d availables cores, %d needed" % (NB_CORES - get_nb_cores_running(), nb_cores))
		return enough_on_server and enough_for_user
	else:
		print("Empty queue")
		return False


def mark_success(object):
	object.status = "EN"
	object.save()
	update_queue()

def mark_error(object, e=None):
	object.status = "ER"
	# object.error = e.message()
	object.save()
	update_queue()

def optim_success(object, optim):

	if optim.isInterrupted():
		object.status = Optimization.INTERRUPTED
	else:
		object.status = Optimization.ENDED
	object.save()
	update_queue()

def optim_error(object, optim, error):
	mark_error(object, error)

def cont_success(object, result):
	object.result = dumps(result).decode('Latin-1')
	object.status = "EN"
	object.save()
	update_queue()


def execute_next_computation():
	print("Executing next computation !")
	next_computation = get_next_computation()
	if next_computation.type == ComputationQueue.OPTIM:
		optimization = Optimization.objects.get(id=next_computation.computation_id)
		optim = loads(next_computation.object.encode('Latin-1'))
		optim.run_async(
			success=lambda executed_optim: optim_success(optimization, executed_optim),
			failure=lambda executed_optim, error=None: optim_error(optimization, executed_optim, error),
			nb_procs=optimization.cores
		)
		optimization.status = Optimization.BUSY
		optimization.save()
		next_computation.delete()
		print("Optimization executed")

	else:
		continuation = Continuation.objects.get(id=next_computation.computation_id)
		cont = loads(next_computation.object.encode('Latin-1'))
		cont.run_async(
			lambda res: cont_success(continuation, res),
			lambda error=None: mark_error(continuation, error)
		)
		continuation.status = Continuation.BUSY
		continuation.save()
		next_computation.delete()
		print("Continuation executed")

def update_queue():

	if can_execute_next_computation():
		execute_next_computation()
		update_queue()

