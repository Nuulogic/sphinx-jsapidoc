sphinx-jsapidoc
=====================

A standalone script for sphinx that works similar to sphinx-autodoc on python files, but iterates through javascript files.
Requires that documentation be marked with a python-style docstring `/*"""`

Warning
-------
Alpha state! And currently does not output for undocumented methods.


Requirements
------------

Pure javascript with a standard javascript paradigm. sphinx-jsapidoc expects that your Javascript is written like so:

    /*"""
     * This is the standard info for the class and its constructor.
     *
     * :param string anArgument: Argument info is placed here. Generally all the standard sphinx stuff works.
     * :param name.of.namespace.OtherClass otherClassObject: Sphinx will even do the lookup of types you specify.
     * :param name.of.namespace.AnotherClass andAnotherThing: If you reference using :class:`path.to.Class`, sphinx-jsapidoc will translate it to the :js: domain.
     */
    name.of.namespace.ClassName = function(anArgument, otherClassObject, andAnotherThing) {

        /*"""
         * Docstrings on attributes in the constructor (or any method actually) that match this.attrName = (.+?) will be captured as attributes.
         */
         this.attrName = "a string.";
    }

    //if you provide a prototype pointing to a "new Class", then sphinx-jsapidoc adds an 'extends ' note to the documentations.
    name.of.namespace.ClassName.prototype = new name.of.BaseClass();
    name.of.namespace.ClassName.constructor = name.of.namespace.ClassName;

    /*"""
     * Instance methods need to be defined like this. sphinx-jsapidoc doesn't yet know how to parse instance methods that are in object notation.
     * 
     * :param string newArg: Set them args like you want to.
     */
    name.of.namespace.ClassName.prototype.newMethod = function(newArg) {

    }

    /*"""
     * Class constants can be documented but will be set as a js:attr.
     */
    name.of.namespace.ClassName.CLASS_CONSTANT = "JustAClassConstant";

    /*"""
     * Static methods are captured, too.
     */
    name.of.namespace.ClassName.staticMethod = function() {

    }

    // this method won't show up in documentation because the comment doesn't start with /*""" 
    /* Javascript is too dynamic of a language to build a reliable abstract syntax tree that will allow
     * a machine to deduce what the developer intended.
     */ 
    name.of.namespace.ClassName.prototype.undocumentedInstanceMethod = function() {

    }

    // the following method will appear in the documentation, but blank.
    /*"""
     * 
     */
    name.of.namespace.ClassName.prototype.documentedInstanceMethod = function() {

    }


Installation
------------

`$ pip install git+git://github.com/Nuulogic/sphinx-jsapidoc.git`


Generation
----------

- You'll want to go through the steps of setting up `sphinx-quickstart` first. The output from `sphinx-jsapidoc` is meant to be dropped into the documentation's source directory (Not the javascript source, but the source quickstart creates.)
- Run these things once your code is documented: `$ ./sphinx-jsapidoc --output-dir /path/to/docs/documentation/source/ /path/to/source/files/with/js/must/be/a/directory/`
- Add `jsmodules` to the `toctree` in your `index.rst`
- When you `make html` sphinx should do it's normal bits



Thanks!
-------

Good luck. And report them bugs. Also, fork this as needed. We'd love input.

Nuu Logic