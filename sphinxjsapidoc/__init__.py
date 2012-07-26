#!/usr/bin/env python

import re
import os
import glob



def parse_directory(dir, depth=0):
    if os.path.exists(dir):
        dir = os.path.realpath(dir)

    classes = {

    }

    files = os.listdir(dir)
    for filename in files:
        filename = os.path.join(dir, filename)
        if filename.endswith('.js') and not os.path.isdir(filename):
            fh = open(filename)
            fileData = fh.read()
            fh.close()

            new_classes = parse(fileData)
            if new_classes is not None:
                classes = dict(classes.items() + new_classes.items())
        #TODO:
        else:
            new_classes = parse_directory(filename, depth+1)
            if new_classes is not None:
                classes = dict(classes.items() + new_classes.items())

    return classes



#def parse_files(filesArray):


def parse(fileString):
    #get all comments from the fileString and their next line.
    #remember scope
    classes = {

    }

    #gets the docstring style comment and the next line up to the point of assignment (attribute, property, or function creation)
    comments_regex = re.compile(r'\/\*"""(.+?)\*/(?:\s+?)(.+?)((?:=|\:?)(?:\s*?)function\((.*?)\)|=|\:|\{|;)', re.M + re.S)
    leading_asterisks = re.compile(r'\n(?:\s*?)\*')

    comment_matches = comments_regex.findall(fileString)

    #current_class is assigned when a class is discovered, but it also is used in the event of a "this" assignment
    current_class = None
    for match in comment_matches:
        #print(match)
        docstring = leading_asterisks.sub('\n', match[0])

        label = match[1]
        if label is not None:
            label = label.strip()

        short_name = label[label.rfind('.')+1:len(label)]
        namespace = label[0:label.rfind('.')]

        assignment = match[2]

        #is this a function?
        if 'function(' in assignment:
            #params might be in the assignment
            params = match[3]

            #is this function a class?
            # if it doesn't contain 'prototype', find out by searching for the label + .prototype
            if '.prototype' not in label:
                if label + '.prototype' in fileString:
                    current_class = JSClassDictionary(label, namespace=namespace, docstring=docstring, short_name=short_name)
                    #if so then this is probably the constructor
                    current_class.constructor = JSFunctionDictionary(label, current_class, docstring)
                    if params is not None:
                        params_list = params.split()
                        for param in params_list:
                            current_class.constructor.params.append(param.strip(','))
                    #there could be a base class. look for it by taking the label + 'constructor'
                    base_class_assignment = re.search(label+'\.prototype = new (.+?)\(', fileString)
                    if base_class_assignment is not None:
                        base_class_name = base_class_assignment.group(1)
                        current_class.base = base_class_name

                    #add the class to the classes dict
                    classes[label] = current_class
                else:
                    #it's a static method if the namespace here is actually the name of an existing class.
                    if namespace not in classes:
                        #could be intended to be a static class
                        if '.' in namespace:
                            static_class_namespace = namespace[0:namespace.rfind('.')]
                        else:
                            static_class_namespace = namespace
                        classes[namespace] = JSClassDictionary(namespace, static_class_namespace)

                    owning_class = classes[namespace]
                    static_method = JSFunctionDictionary(label, owning_class, docstring, short_name)
                    if params is not None:
                        params_list = params.split()
                        for param in params_list:
                            static_method.params.append(param.strip(','))

                    owning_class.static_methods.append(static_method)

            else:
                # if it does contain 'prototype', it's part of a class, but just an instance method
                class_name = label[0:label.rfind('.prototype')]

                if class_name in classes:
                    owning_class = classes[class_name]
                    instance_method = JSFunctionDictionary(short_name, owning_class, docstring)
                    #the params might be in the function. they're nice-to-haves
                    if params is not None:
                        params_list = params.split()
                        for param in params_list:
                            instance_method.params.append(param.strip(','))

                    owning_class.methods.append(instance_method)

        elif namespace == 'this' and current_class is not None:
            #this is a documented instance attribute that is inside a function. Most people put them in the constructor.
            attribute = JSAttributeDictionary(short_name, current_class, docstring)
            current_class.attributes.append(attribute)

        elif '.prototype' in namespace:
            #this is a documented instance attribute that is not inside a function.
            namespace = namespace[0:namespace.rfind('.prototype')]

            if namespace in classes:
                owning_class = classes[namespace]
                attribute = JSAttributeDictionary(short_name, owning_class, docstring)
                owning_class.attributes.append(attribute)

        else:
            #probably a static class's static attribute:
            # to find out. see if there is a prototype.
            if label + '.prototype' not in fileString:
                if label not in classes:
                    #could be intended to be a static class
                    #static_class_namespace = namespace[0:namespace.rfind('.')]
                    classes[label] = JSClassDictionary(label, namespace)

                owning_class = classes[label]
                owning_class.class_attributes.append(JSAttributeDictionary(label, owning_class, docstring))
            else:
                print('Class ' + label + ' has a property assigned to it before being declared.')
            


    return classes


def indent(text, white_space):
    if white_space is None:
        white_space = '    ';
    lines = text.split('\n')
    result = '';
    for line in lines:
        result += white_space + line + '\n'

    return result;

def fix_roles(text):
    #replace all :js:class: with :class: then normalize by replacing all :class: with :js:class:
    return text.replace(':js:class:', ':class:').replace(":class:", ":js:class:").replace(':meth:', ':js:attr:')

def underline(text, char='='):
    underline = ''.center(len(text), char)
    return text + '\n' + underline + '\n'

def sandwich(text, char='='):
    underline = ''.center(len(text), char)
    return underline + '\n' + text + '\n' + underline + '\n'

    
class JSClassDictionary(object):
    def __init__(self, name, namespace='', docstring='', short_name=''): #, constructor=None, attributes=[], methods=[], class_attributes=[], static_methods=[], class_consts=[]):
        self.name = name
        self.short_name = short_name
        self.namespace = namespace
        self.docstring = docstring
        self.constructor = None
        self.base = None
        self.attributes = []
        self.methods = []
        #print(', '.join([i.name for i in methods]))
        self.class_attributes = []
        self.static_methods = []
        self.class_consts = []

class JSFunctionDictionary():
    def __init__(self, name, class_dictionary=None, docstring='', short_name=''): #, params=[], code=''):
        self.name = name
        self.short_name = short_name
        self.class_dictionary = class_dictionary
        self.docstring = docstring
        self.params = []
        self.code = ''

class JSAttributeDictionary():
    def __init__(self, name, class_dictionary=None, docstring=''):
        self.name = name
        self.class_dictionary = class_dictionary
        self.docstring = docstring
