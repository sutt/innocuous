Update the tests to pass for the following failures. 

The test previously passed before the changes listed below.

============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/user/dev/innocuous/demo-llama
configfile: pyproject.toml
testpaths: tests
plugins: mock-3.14.1
collected 21 items

tests/test_cli.py FFFFFFFFFFFF                                           [ 57%]
tests/test_simple.py .........                                           [100%]

=================================== FAILURES ===================================
_______________________________ test_encode_text _______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f69993541a0>

    def test_encode_text(mocker):
        """Test encode command with --text."""
        mocker.patch("sys.argv", ["innocuous", "encode", "--text", "hello"])
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
>       mock_create_llm = mocker.patch("stego_llm.cli.create_llm_client")
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_cli.py:12: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984ed7830>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
______________________________ test_encode_bytes _______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6985559490>

    def test_encode_bytes(mocker):
        """Test encode command with --bytes."""
        mocker.patch(
            "sys.argv", ["innocuous", "encode", "--bytes", "68656c6c6f"]
        )  # "hello" in hex
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:28: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f699931d6a0>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_____________________________ test_encode_btc_addr _____________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f05d60>

    def test_encode_btc_addr(mocker):
        """Test encode command with --btc-addr."""
        addr = "bc1q..."
        mocker.patch("sys.argv", ["innocuous", "encode", "--btc-addr", addr])
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode", return_value="encoded")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:42: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f698555b530>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_____________________________ test_decode_message ______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f07890>

    def test_decode_message(mocker):
        """Test decode command with --message."""
        mocker.patch(
            "sys.argv", ["innocuous", "decode", "--message", "some encoded message"]
        )
        mock_main_decode = mocker.patch(
            "stego_llm.cli.main_decode", return_value=b"decoded"
        )
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:59: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f698555b170>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________________ test_decode_file _______________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f06f60>
tmp_path = PosixPath('/tmp/pytest-of-user/pytest-8/test_decode_file0')

    def test_decode_file(mocker, tmp_path):
        """Test decode command with --file."""
        p = tmp_path / "message.txt"
        p.write_text("file encoded message")
        mocker.patch("sys.argv", ["innocuous", "decode", "--file", str(p)])
        mock_main_decode = mocker.patch(
            "stego_llm.cli.main_decode", return_value=b"decoded"
        )
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:76: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6985765b80>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
___________________________ test_initial_prompt_text ___________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2a600>

    def test_initial_prompt_text(mocker):
        """Test --initial-prompt-text flag."""
        mocker.patch(
            "sys.argv",
            ["innocuous", "--initial-prompt-text", "my prompt", "encode", "--text", "t"],
        )
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:92: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f699bdcc470>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
___________________________ test_initial_prompt_file ___________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2d8b0>
tmp_path = PosixPath('/tmp/pytest-of-user/pytest-8/test_initial_prompt_file0')

    def test_initial_prompt_file(mocker, tmp_path):
        """Test --initial-prompt-file flag."""
        p = tmp_path / "prompt.txt"
        p.write_text("prompt from file")
        mocker.patch(
            "sys.argv",
            ["innocuous", "--initial-prompt-file", str(p), "encode", "--text", "t"],
        )
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:110: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f698555b710>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________________ test_chunk_size ________________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2df10>

    def test_chunk_size(mocker):
        """Test --chunk_size flag."""
        mocker.patch(
            "sys.argv", ["innocuous", "--chunk_size", "4", "encode", "--text", "t"]
        )
        mock_main_encode = mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:125: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f31970>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg0-30] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2d610>
verbose_arg = [], expected_level = 30

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f2c440>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg1-20] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2e9c0>
verbose_arg = ['-v'], expected_level = 20

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f699be35550>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg2-10] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f2b6b0>
verbose_arg = ['-vv'], expected_level = 10

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f06f30>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
_______________________ test_verbosity[verbose_arg3-10] ________________________

mocker = <pytest_mock.plugin.MockerFixture object at 0x7f6984f33710>
verbose_arg = ['-vvv'], expected_level = 10

    @pytest.mark.parametrize(
        "verbose_arg, expected_level",
        [
            ([], logging.WARNING),
            (["-v"], logging.INFO),
            (["-vv"], logging.DEBUG),
            (["-vvv"], logging.DEBUG),
        ],
    )
    def test_verbosity(mocker, verbose_arg, expected_level):
        """Test verbosity flags."""
        argv = ["innocuous"] + verbose_arg + ["encode", "--text", "t"]
        mocker.patch("sys.argv", argv)
        mocker.patch("stego_llm.cli.main_encode")
>       mocker.patch("stego_llm.cli.create_llm_client")

tests/test_cli.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:439: in __call__
    return self._start_patch(
.venv/lib/python3.12/site-packages/pytest_mock/plugin.py:257: in _start_patch
    mocked: MockType = p.start()
                       ^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1624: in start
    result = self.__enter__()
             ^^^^^^^^^^^^^^^^
../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1467: in __enter__
    original, local = self.get_original()
                      ^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <unittest.mock._patch object at 0x7f6984f8d910>

    def get_original(self):
        target = self.getter()
        name = self.attribute
    
        original = DEFAULT
        local = False
    
        try:
            original = target.__dict__[name]
        except (AttributeError, KeyError):
            original = getattr(target, name, DEFAULT)
        else:
            local = True
    
        if name in _builtins and isinstance(target, ModuleType):
            self.create = True
    
        if not self.create and original is DEFAULT:
>           raise AttributeError(
                "%s does not have the attribute %r" % (target, name)
            )
E           AttributeError: <module 'stego_llm.cli' from '/home/user/dev/innocuous/demo-llama/stego_llm/cli.py'> does not have the attribute 'create_llm_client'

../../../.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/unittest/mock.py:1437: AttributeError
=========================== short test summary info ============================
FAILED tests/test_cli.py::test_encode_text - AttributeError: <module 'stego_l...
FAILED tests/test_cli.py::test_encode_bytes - AttributeError: <module 'stego_...
FAILED tests/test_cli.py::test_encode_btc_addr - AttributeError: <module 'ste...
FAILED tests/test_cli.py::test_decode_message - AttributeError: <module 'steg...
FAILED tests/test_cli.py::test_decode_file - AttributeError: <module 'stego_l...
FAILED tests/test_cli.py::test_initial_prompt_text - AttributeError: <module ...
FAILED tests/test_cli.py::test_initial_prompt_file - AttributeError: <module ...
FAILED tests/test_cli.py::test_chunk_size - AttributeError: <module 'stego_ll...
FAILED tests/test_cli.py::test_verbosity[verbose_arg0-30] - AttributeError: <...
FAILED tests/test_cli.py::test_verbosity[verbose_arg1-20] - AttributeError: <...
FAILED tests/test_cli.py::test_verbosity[verbose_arg2-10] - AttributeError: <...
FAILED tests/test_cli.py::test_verbosity[verbose_arg3-10] - AttributeError: <...
========================= 12 failed, 9 passed in 0.93s =========================

Changes that caused the test failure.


commit 55cf7ce3a3b6910826b0c267cc517fad792c08aa
Author: sutt <wsutton17@gmail.com>
Date:   Mon Aug 25 20:39:12 2025 -0400

    feat: allow specifying LLM path via CLI arg or env var

diff --git a/stego_llm/cli.py b/stego_llm/cli.py
index 7f3653f..16569bf 100644
--- a/stego_llm/cli.py
+++ b/stego_llm/cli.py
@@ -4,7 +4,6 @@ import sys
 from pathlib import Path
 
 from stego_llm.core import main_decode, main_encode
-from stego_llm.llm import create_llm_client
 
 logger = logging.getLogger(__name__)
 
@@ -15,6 +14,7 @@ def main():
     parser.add_argument(
         "-v", "--verbose", action="count", default=0, help="Increase verbosity"
     )
+    parser.add_argument("--llm-path", type=Path, help="Path to LLM GGUF file")
     parser.add_argument(
         "--chunk_size", type=int, default=3, help="Chunk size for encoding/decoding"
     )
@@ -75,13 +75,12 @@ def main():
         elif args.btc_addr:
             message_bytes = args.btc_addr.encode("utf-8")
 
-        llm = create_llm_client()
         encoded_message = main_encode(
-            llm=llm,
             initial_prompt=initial_prompt,
             msg=message_bytes,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(encoded_message)
 
@@ -92,13 +91,12 @@ def main():
         elif args.file:
             encoded_text = args.file.read_text()
 
-        llm = create_llm_client()
         decoded_bytes = main_decode(
-            llm=llm,
             encoded_prompt=encoded_text,
             initial_prompt=initial_prompt,
             chunk_size=args.chunk_size,
             num_logprobs=num_logprobs,
+            llm_path=args.llm_path,
         )
         print(repr(decoded_bytes))
 
diff --git a/stego_llm/core/decoder.py b/stego_llm/core/decoder.py
index a8f6045..5b20748 100644
--- a/stego_llm/core/decoder.py
+++ b/stego_llm/core/decoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_decoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_decode(
-    llm,
     encoded_prompt,
     initial_prompt,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main decoding function for steganographic message extraction."""
+    llm = create_llm_client(model_path=llm_path)
     message_carrying_text = encoded_prompt[len(initial_prompt) :]
     memo = {}
 
diff --git a/stego_llm/core/encoder.py b/stego_llm/core/encoder.py
index 3cf5a44..4b6e5ea 100644
--- a/stego_llm/core/encoder.py
+++ b/stego_llm/core/encoder.py
@@ -5,7 +5,11 @@ from stego_llm.steganography import (
     pre_selection_filter,
     post_selection_filter,
 )
-from stego_llm.llm import get_token_probabilities, logits_to_probabilities
+from stego_llm.llm import (
+    create_llm_client,
+    get_token_probabilities,
+    logits_to_probabilities,
+)
 from .trace import _trace_encoding_step
 
 
@@ -13,13 +17,14 @@ logger = logging.getLogger(__name__)
 
 
 def main_encode(
-    llm,
     initial_prompt,
     msg,
     chunk_size,
     num_logprobs,
+    llm_path=None,
 ):
     """Main encoding function for steganographic text generation."""
+    llm = create_llm_client(model_path=llm_path)
     enc_ints = message_to_chunks(msg, chunk_size=chunk_size)
     current_prompt = initial_prompt
 
diff --git a/stego_llm/llm/interface.py b/stego_llm/llm/interface.py
index 81a28a0..31e2828 100644
--- a/stego_llm/llm/interface.py
+++ b/stego_llm/llm/interface.py
@@ -1,4 +1,5 @@
 import json
+import os
 import numpy as np
 from llama_cpp import Llama
 from .utilities import suppress_stderr, logits_to_probabilities, to_json
@@ -6,9 +7,14 @@ from .utilities import suppress_stderr, logits_to_probabilities, to_json
 
 @suppress_stderr
 def create_llm_client(
-    model_path="/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+    model_path=None,
 ):
     """Initialize and return a Llama LLM client."""
+    if model_path is None:
+        model_path = os.environ.get(
+            "INNOCUOUS_LLM_PATH",
+            "/home/user/dev/innocuous/data/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
+        )
     return Llama(
         model_path=model_path,
         logits_all=True,
