from functools import wraps
from .observer import Observer, ObserversList


def observe_models(*models):
    """
    Decorator used to add model observers to function/method decorated
    :param models: the models to be observed
    """
    def decorator(observed_method):
        @wraps(observed_method)
        def wrapper(this, *args, **kwargs):
            this.observers = ObserversList()
            # connect signals
            for model in models:
                observer = Observer(model)
                observer.connect()
                this.observers[model] = observer
                # add this.modelname_observer property
                observer.monkey_patch_observer(this)
            # add default observer
            if len(models) == 1:
                this.observer = this.observers[models[0]]

            try:
                # execute method itself
                observed_method(this, *args, **kwargs)
            except Exception:
                raise
            finally:
                # disconnect all signals in any case
                for observer in this.observers.values():
                    observer.disconnect()

        return wrapper
    return decorator


# TODO self.observers.assertNothingHasChanged
# TODO with statement
# TODO add receiver to signal `m2m_changed`
