from RestrictedPython import compile_restricted, safe_builtins, utility_builtins, safe_globals
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
from RestrictedPython.Guards import full_write_guard, guarded_iter_unpack_sequence, guarded_unpack_sequence
import strategy

def get_securely_wrapped_class(file_path: str) -> strategy.Strategy:
    with open(file_path) as f:
        code = f.readlines()
    #delete imports
    code = [line for line in code if not (line.startswith("from"))]
    code = [line for line in code if not (line.startswith("import"))]
    code = "".join(code)
    # code = open("strategy.py").read()+"\n"+code
    local_dict = {}
    my_builtins = safe_builtins.copy()
    my_builtins.update(utility_builtins)
    global_dict = {**safe_globals, **utility_builtins, "__metaclass__": type,
                   "__name__": file_path,
                   "__builtins__": my_builtins,
                   "_write_": lambda x: x if isinstance(x, strategy.Strategy) else full_write_guard(x),
                   "_getattr_": getattr,
                   "Strategy": strategy.Strategy,
                   "strategy": strategy,
                   "_getiter_": default_guarded_getiter,
                   "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
                   "_unpack_sequence_": guarded_unpack_sequence,
                   "_getitem_": default_guarded_getitem,
                   }
    exec(compile_restricted(code, '<string>', 'exec'), global_dict, local_dict)
    global_dict.update(local_dict)
    return local_dict['MyStrategy']