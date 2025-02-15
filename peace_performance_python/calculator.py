from .types import NativeCalculator
from .pp_result import CalcResult
from .beatmap import Beatmap

from ._peace_performance import pp as _pp_rust

from typing import Any, Callable, Dict, Optional, Tuple, Union


class Calculator:
    '''
    Calculator for storing pp calculation configurations (mode, mods, combo, 300, miss, acc, etc.)

    ### Examples:
    ```
    beatmap = await Beatmap('path_to_osu_file')
    c = Calculator()
    c.set_acc(98.8)
    c.set_combo(727)
    # or
    c = Calculator({'acc': 98.8, 'combo': 727})
    # then
    result = c.calculate(beatmap)
    ```
    '''
    _raw_attrs = ('mode', 'mods', 'n50', 'n100', 'n300',
                  'katu', 'acc', 'passed_obj', 'combo', 'miss',)
    _extra_attrs = ('_raw',)
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeCalculator
    mode: Optional[int]
    mods: Optional[int]
    n50: Optional[int]
    n100: Optional[int]
    n300: Optional[int]
    katu: Optional[int]
    acc: Optional[float]
    passed_obj: Optional[int]
    combo: Optional[int]
    miss: Optional[int]

    def __new__(cls, *_, **__) -> 'Calculator':
        cls.__init_property__()
        obj: 'Calculator' = super().__new__(cls)
        return obj

    def __init__(self, data: Optional[Dict[str, Union[int, float, None]]] = None, **kwargs) -> 'Calculator':
        '''Create new Calculator'''
        self._raw = _pp_rust.Calculator()
        set = data or kwargs
        if set:
            self.set_with_dict(set)

    def __repr__(self) -> str:
        return f'<Calculator object ({self.attrs})>'

    @classmethod
    def __init_property__(cls) -> None:
        '''Initial property and methods'''
        for attr in cls._raw_attrs:
            handlers = cls.__property_handlers__(attr)
            for prefix, handler in zip(('get_', 'set_', 'del_',), handlers):
                setattr(cls, prefix + attr, handler)
            setattr(cls, attr, property(*handlers))

    @staticmethod
    def __property_handlers__(attr: str) -> Tuple[Callable[['Calculator'], Any]]:
        '''Returns getter, setter and deleter methods for attr'''
        def _getter_wrapper(c: 'Calculator') -> Any:
            return c.getattr(attr)

        def _setter_wrapper(c: 'Calculator', value) -> None:
            return c.setattr(attr, value)

        def _deleter_wrapper(c: 'Calculator') -> None:
            return c.setattr(attr, None)

        return (_getter_wrapper, _setter_wrapper, _deleter_wrapper,)

    def __clear_calc_attrs__(self) -> None:
        '''Clear all calc attr'''
        for attr in self._raw_attrs:
            self.setattr(attr, None)

    def getattr(self, attr) -> Any:
        return getattr(self._raw, attr)

    def setattr(self, attr, value) -> None:
        return setattr(self._raw, attr, value)

    @property
    def attrs(self) -> str:
        return ', '.join([f'{attr}: {self.getattr(attr)}'
                          for attr in self._raw_attrs])

    def reset(self) -> None:
        '''Set self to the default state'''
        self._raw.reset()
        self.__clear_calc_attrs__()

    def set_with_dict(self, data: Dict[str, Any]) -> None:
        '''
        Set data with a dict.

        ### Examples:
        ```
        data = {
            'mode': 0,
            'n50': 66,
            'n100': 666
        }
        c = Calculator()
        c.set_with_dict(data)
        # or
        c = Calculator(data)
        ```
        '''
        for attr, value in data.items():
            self.setattr(attr, value)

    def calculate(self, beatmap: 'Beatmap') -> 'CalcResult':
        '''
        Calculate pp with a Beatmap.

        ### Examples:
        ```
        beatmap = await Beatmap('path_to_osu_file')
        c = Calculator()
        c.set_acc(98.8)
        c.set_combo(727)
        # or
        c = Calculator({'acc': 98.8, 'combo': 727})
        # then
        result = c.calculate(beatmap)
        ```
        '''
        return CalcResult(self._raw.calculate(beatmap._raw))

    # Interfaces -----
    def set_mode(val: Optional[int]) -> None: ...
    def set_mods(val: Optional[int]) -> None: ...
    def set_n50(val: Optional[int]) -> None: ...
    def set_n100(val: Optional[int]) -> None: ...
    def set_n300(val: Optional[int]) -> None: ...
    def set_katu(val: Optional[int]) -> None: ...
    def set_acc(val: Optional[float]) -> None: ...
    def set_passed_obj(val: Optional[int]) -> None: ...
    def set_combo(val: Optional[int]) -> None: ...
    def set_miss(val: Optional[int]) -> None: ...

    def del_mode() -> None: ...
    def del_mods() -> None: ...
    def del_n50() -> None: ...
    def del_n100() -> None: ...
    def del_n300() -> None: ...
    def del_katu() -> None: ...
    def del_acc() -> None: ...
    def del_passed_obj() -> None: ...
    def del_combo() -> None: ...
    def del_miss() -> None: ...

    def get_mode(val: Optional[int]) -> Optional[int]: ...
    def get_mods(val: Optional[int]) -> Optional[int]: ...
    def get_n50(val: Optional[int]) -> Optional[int]: ...
    def get_n100(val: Optional[int]) -> Optional[int]: ...
    def get_n300(val: Optional[int]) -> Optional[int]: ...
    def get_katu(val: Optional[int]) -> Optional[int]: ...
    def get_acc(val: Optional[float]) -> Optional[float]: ...
    def get_passed_obj(val: Optional[int]) -> Optional[int]: ...
    def get_combo(val: Optional[int]) -> Optional[int]: ...
    def get_miss(val: Optional[int]) -> Optional[int]: ...


def new_raw_calculator() -> NativeCalculator:
    '''Create new native calculator'''
    return _pp_rust.new_calculator()


def calculate_pp(beatmap: Beatmap, calculator: Calculator) -> CalcResult:
    '''Calculate PP with beatmap and calculator'''
    return calculator.calculate(beatmap)
