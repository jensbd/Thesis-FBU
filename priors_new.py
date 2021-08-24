import pymc3 as mc
priors = {
    }

def wrapper(priorname='',low=[],up=[],other_args={},optimized=False):
    # Suggested changes are in blocks enclosed by #---# borders
    #--------------------------------------------------------------------------#
    # Get non-keyword arguments from other_args, return empty list if not found
    non_kwargs = other_args.get('non_kwargs', [])
    #--------------------------------------------------------------------------#

    if priorname in priors: 
        priormethod = priors[priorname] 
    elif hasattr(mc,priorname):
        priormethod = getattr(mc,priorname)
    else:
        print( 'WARNING: prior name not found! Falling back to DiscreteUniform...' )
        priormethod = mc.DiscreteUniform

    truthprior = []
    #--------------------------------------------------------------------------#
    # If the Interpolated class is to be used, use arguments from non_kwargs
    if priorname == 'Interpolated':
        for bin,(l,u) in enumerate(zip(low,up)):
            name = 'truth%d'%bin
            prior = priormethod(name, non_kwargs[0][bin], non_kwargs[1][bin])
            truthprior.append(prior)
    else:
    #--------------------------------------------------------------------------#
        for bin,(l,u) in enumerate(zip(low,up)):
            name = 'truth%d'%bin
            default_args = dict(name=name,lower=l,upper=u)
            args = dict(list(default_args.items())+list(other_args.items()))
            prior = priormethod(**args)
            truthprior.append(prior)

    return mc.math.stack(truthprior) #https://github.com/pymc-devs/pymc3/issues/502
