@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=docsrc
set BUILDDIR=_build

if "%1" == "" goto help

if "%1" == "github" (
	coverage run -m pytest test --html=docs/_static/test_report.html
	
	%SPHINXBUILD% -b html %SOURCEDIR% %SOURCEDIR% %BUILDDIR%
    sphinx-apidoc -o docsrc src
    %SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
    robocopy %BUILDDIR%/html ../docs /E > nul
    echo.Generated files copied to ../docs
	coverage report -m 

    goto end
)

if "%1" == "help" (
	echo.docs:			generates/update documentation.
	echo.test:			executes unit testing.
	echo.generate_test: use pynguin to create new test cases.
	echo.github:		gets ready project prior to git push.

    goto end
)

if "%1" == "docs" (
	%SPHINXBUILD% -v -b coverage %SOURCEDIR% %BUILDDIR%/coverage
	%SPHINXBUILD% -b html %SOURCEDIR% %SOURCEDIR% %BUILDDIR%
    sphinx-apidoc -o docsrc src
    %SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
    robocopy %BUILDDIR%/html ../docs /E > nul
    echo.Generated files copied to ../docs

    goto end
)

if "%1" == "test" (
	rem execute doctests.
	pytest --doctest-modules src

	rem Beautify source code by using 'black' and 'autopep8' tools
	black src
	autopep8.exe src\ --recursive --in-place --pep8-passes 2000 --verbose
	
	rem https://breadcrumbscollector.tech/how-to-use-code-coverage-in-python-with-pytest/
	rem https://medium.com/swlh/unit-testing-in-python-basics-21a9a57418a0
	rem pytest --flake8 --black src
	coverage run -m pytest test --html=docs/_static/test_report.html --mypy --mccabe --cov-branch --cov-report term-missing
	coverage report -m 

	rem https://pypi.org/project/docstr-coverage/
	docstr-coverage --skip-file-doc --skip-init --exclude ".*/docs" --badge=docsrc/image/docstr-cov.svg src

    goto end
)

if "%1" == "generate_test" (
	rem https://www.youtube.com/watch?v=hLA9Q4tSkMU
	pynguin.exe --project_path ./src --output_path ./test --module_name game_rules --create_coverage_report true --budget 15 --seed 20220225 --type_inference_strategy TYPE_HINTS --use-archive True --seed_from_archive True --filter_covered_targets_from_test_cluster True -v
    pynguin.exe --project_path ./src --output_path ./test --module_name player --create_coverage_report true --budget 15 --seed 20220225 --type_inference_strategy TYPE_HINTS --use-archive True --seed_from_archive True --filter_covered_targets_from_test_cluster True -v
    pynguin.exe --project_path ./src --output_path ./test --module_name ui --create_coverage_report true --budget 15 --seed 20220225 --type_inference_strategy TYPE_HINTS --use-archive True --seed_from_archive True --filter_covered_targets_from_test_cluster True -v
    pynguin.exe --project_path ./src --output_path ./test --module_name state --create_coverage_report true --budget 15 --seed 20220225 --type_inference_strategy TYPE_HINTS --use-archive True --seed_from_archive True --filter_covered_targets_from_test_cluster True -v

    goto end
)



%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
