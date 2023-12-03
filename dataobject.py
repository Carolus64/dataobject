from dataclasses import dataclass, field
from typing import Union

#@dataclass
#class binarydo:
#    data: bytearray = None
#    l: int = field(init=False)
#    lmax: int = 0
#
#    def __post_init__(self):
#        self.l = 0 if self.data is None else len(self.data)
#        if self.lmax > 0 and self.l > self.lmax:
#            raise ValueError('Data buffer length greater than max size')
#
#    @classmethod
#    def frombytes(cls, buf: bytearray, max: int =0):
#        if max==0:
#            bdo = cls(buf, 0)
#        else:
#            llen = 2
#            if max>99:
#                llen = 3
#            l = (int)(buf[:llen].decode('ascii'))
#            bdo = cls(buf[llen:llen+l], max)
#        return bdo
#
#    @classmethod
#    def fromhex(cls, s: str, max: int =0):
#        buf = bytes.fromhex(s)
#        return cls.frombytes(buf, max)
#
#    def __str__(self):
#        s = f"l={self.l} lmax={self.lmax}"
#        if not self.data is None:
#            s += f" data:{self.data.hex(' ')}"
#        return s

#@dataclass
#class binarydo2:
#    data: bytearray = None
#    lmin: int = 0
#    lmax: int = 0
#
#    def __post_init__(self):
#        if self.lmin < 0:
#            raise ValueError('min length cannot be negative')            
#        if self.lmax < 0:
#            raise ValueError('max length cannot be negative')            
#        l = 0 if self.data is None else len(self.data)
#        if self.lmax == 0:
#            if self.lmin == 0:
#                self.lmin = self.lmax = l
#            else:
#                if l != self.lmin:
#                    raise ValueError('Invalid data buffer length')            
#                self.lmin = self.lmax = l
#        else:
#            if l < self.lmin:
#                raise ValueError('Data buffer length smaller than min size')
#            if l > self.lmax:
#                raise ValueError('Data buffer length greater than max size')                                         
#                
#    def __str__(self):
#        s = f"lmin={self.lmin} lmax={self.lmax}"
#        if not self.data is None:
#            s += f" data:{self.data.hex(' ')}"
#        else:
#            s += " Empty"
#        return s

class do:
    def __init__(self, type: str ='b', var: bool = True, length: int = 256, data: Union[bytearray, str, int] = None):
        self.type = type
        self.isvar = var        
        if length < 0:
            raise ValueError('illegal negative length')
        self.l = length
        self.Set(data)
    
    def Set(self, value: Union[bytearray, str, int]):
        if value:
            if self.type == 'b':
                # binary dataobject
                if not isinstance(value, bytes):
                    raise ValueError('invalid type for data')
                self.data = value[:self.l]
                # se lunghezza fissa e più piccolo: esegue pad a destra con bytes 0x00
                if not self.isvar:
                    if len(self.data) < self.l:
                        self.data += bytes(self.l - len(self.data))
            elif self.type == 'n':
                # numeric dataobject
                if isinstance(value, str):
                    if not value.isnumeric():
                        raise ValueError("Error, setting non numeric data to 'n' dataobject")
                    self.data = value[:self.l]
                elif isinstance(value, int):
                    self.data = str(value)
                else:
                    raise ValueError('invalid type for data')
                # se lunghezza fissa e più piccolo: esegue pad a sinistra con '0'
                if not self.isvar:
                    if len(self.data) < self.l:
                        self.data = ('0' * (self.l - len(self.data))) + self.data
            elif self.type == 'a' or self.type == 'an' or self.type == 'ans':
                # alphanumeric or alphanumeric special dataobject
                if not isinstance(value, str):
                    raise ValueError('invalid type for data')
                if self.type == 'a' and not value.isalpha():
                    raise ValueError("Error, setting non alpha data to 'a' dataobject")
                if self.type == 'an' and not value.isalnum():
                    raise ValueError("Error, setting non alphanumeric data to 'an' dataobject")
                self.data = value[:self.l]
                # se lunghezza fissa e più piccolo: esegue pad a destra con blanks
                if not self.isvar:
                    if len(self.data) < self.l:
                        self.data += (' ' * (self.l - len(self.data)))                   
        else:
            self.data = None

    @classmethod
    def parse(cls, type: str, var: bool, length: int, buf: bytearray):
        d = cls(type, var, length)
        if var:
            ll = 2
            if length > 99:
                ll = 3
                
            pass
        else:
            if type == 'n':
                pass
            else:
                d.Set(buf[:length])
        return d

    
    def __str__(self):
        if self.isvar:
            s = f'"{self.type}..{self.l}"'
        else:
            s = f'"{self.type}{self.l}"'
        if self.data:
            if self.type == 'b':
                s += f" data:{self.data.hex(' ')}"
            else:
                s += f" data:'{self.data}'"
        else:
            s += " Empty"
        return s

class binarydo(do):
    def __init__(self, var: bool = True, length: int = 256, data: bytearray = None):
        super().__init__('b', var, length, data)

class numericdo(do):
    def __init__(self, var: bool = True, length: int = 256, data: Union[str, int] = None):
        super().__init__('n', var, length, data)

class alphanumdo(do):
    def __init__(self, var: bool = True, length: int = 256, data: Union[str, int] = None):
        super().__init__('an', var, length, data)

class alphanumsdo(do):
    def __init__(self, var: bool = True, length: int = 256, data: Union[str, int] = None):
        super().__init__('ans', var, length, data)
        
#def __test1():
#    print("Testing binarydo")
#    bdo1 = binarydo()
#    print(bdo1)
#    bdo2 = binarydo(b'\x43\xAF\xCC')
#    print(bdo2)
#    bdo3 = binarydo(b'\xCA\xFF\xEE\x01\x02\x03', 19)
#    print(bdo3)
#    
#    # lunghezza fissa da buffer binari
#    bdo4 = binarydo.frombytes(b'\x12\x34\x56')
#    print(bdo4)
#    bdo5 = binarydo.fromhex('789ABCDE')
#    print(bdo5)
#    # lunghezza variabile da buffer binari
#    buf = b'12' + bytes(12)
#    bdo6 = binarydo.frombytes(buf, 20)
#    print(bdo6)
#    buf = b'105' + bytes(105)
#    bdo7 = binarydo.frombytes(buf, 999)
#    print(bdo7)

#def __test2():
#    print("Testing binarydo2")
#    bdo1 = binarydo2()
#    print(bdo1)
#    bdo2 = binarydo2(b'\x43\xAF\xCC')
#    print(bdo2)
#    bdo3 = binarydo2(b'\x12\x34\x56\x78', 4)
#    print(bdo3)
#    bdo4 = binarydo2(b'\x12\x34\x56\x78\x9A\xBC\xde\xff', lmax=7)
#    print(bdo4)

def __test3():
    print("Testing do")
    # binary do
    print("binary dataobject")
    d1 = do()
    print(d1)
    d2 = do(length=8)
    print(d2)
    d3 = do(var=False, length=8)
    print(d3)
    # Initializing with data
    d4 = do(length=5, data=b'123')
    print(d4)
    d5 = do(length=5, data=b'123456789')
    print(d5)
    d6 = do(length=5, var=False, data=b'123')
    print(d6)
    d7 = do(length=5, var=False, data=b'123456789')
    print(d7)
    # check data type
    try:
        d8 = do(length=5, data='123')
        print(d8)
    except ValueError as vex:
        print(vex)

    # alphanumeric do   
    print("Alphanumeric dataobject")
    d11 = do(type='an')
    print(d11)
    d12 = do(type='an', length=8)
    print(d12)
    d13 = do(type='an', var=False, length=8)
    print(d13)
    # Initializing with data
    d14 = do(type='an', length=10, data='ABC123')
    print(d14)
    d15 = do(type='an', length=10, data='ABCDE123456789')
    print(d15)
    d16 = do(type='an', length=10, var=False, data='ABC123')
    print(d16)
    d17 = do(type='an', length=10, var=False, data='ABCDE123456789')
    print(d17)
    
    # numeric do
    print("Numeric dataobject")
    d21 = do(type='n')
    print(d21)
    d22 = do(type='n', length=8)
    print(d22)
    d23 = do(type='n', var=False, length=8)
    print(d23)
    # Initializing with data
    d24 = do(type='n', length=5, data='123')
    print(d24)
    d25 = do(type='n', length=5, data='123456789')
    print(d25)
    d26 = do(type='n', length=5, data=1234)
    print(d26)
    d27 = do(type='n', length=5, var=False, data='123')
    print(d27)
    d28 = do(type='n', length=5, var=False, data='123456789')
    print(d28)
    d29 = do(type='n', length=5, data=1234)
    print(d29)

    # numeric do (2)
    print("numericdo")
    d31 = numericdo(length=12, data=170364)
    print(d31)
 
    
if __name__ == "__main__":
    __test3()


    