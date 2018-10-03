# File Structure (Full) of the Package pos

```plantuml
@startuml

salt
{
    {T
        pos
        + <&folder> Docs
        ++ <&folder> Design_and_Requirements
        +++ <&document> DE001_Core_Features.md
        ++ <&folder> Problem_Analysis
        +++ <&folder> PA001_Descriptors
        ++++ <&script> pa001_descriptors_test01.py
        ++++ <&script> pa001_descriptors_test02.py
        ++++ <&script> pa001_descriptors_test03.py
        ++++ <&script> pa001_descriptors_test04.py
        ++++ <&script> pa001_descriptors_test05.py
        ++++ <&script> pa001_descriptors_test06.py
        ++++ <&script> pa001_descriptors_test07.py
        ++++ <&script> pa001_descriptors_test08.py
        ++++ <&document> PA001_Descriptors.md
        +++ <&folder> PA002_Decorators
        ++++ <&script> pa002_decorators_test01.py
        ++++ <&script> pa002_decorators_test02.py
        ++++ <&script> pa002_decorators_test03.py
        ++++ <&script> pa002_decorators_test04.py
        ++++ <&script> pa002_decorators_test05.py
        ++++ <&script> pa002_decorators_test06.py
        ++++ <&script> pa002_decorators_test07.py
        ++++ <&script> pa002_decorators_test08.py
        ++++ <&script> pa002_decorators_test09.py
        ++++ <&document> PA002_Decorators.md
        +++ <&folder> PA003_Virtual_Inheritance_Exceptions
        ++++ <&document> PA003_Virtual_Inheritance_Exceptions.md
        ++++ <&script> pa003_virtual_inheritance_test001.py
        ++++ <&script> pa003_virtual_inheritance_test002.py
        ++++ <&script> pa003_virtual_inheritance_test003.py
        ++++ <&script> pa003_virtual_inheritance_test004.py
        +++ <&folder> PA004_Traceback
        ++++ <&document> PA004_Traceback_of_Exceptions.md
        ++++ <&script> pa004_traceback_test001.py
        ++++ <&script> pa004_traceback_test002.py
        ++++ <&script> pa004_traceback_test003.py
        ++++ <&script> pa004_traceback_test004.py
        ++++ <&script> pa004_traceback_test005.py
        ++++ <&script> pa004_traceback_test006.py
        ++++ <&script> pa004_traceback_test007.py
        ++++ <&script> pa004_traceback_test008.py
        ++++ <&script> pa004_traceback_test009.py
        ++++ <&script> pa004_traceback_test010.py
        ++++ <&script> pa004_traceback_test011.py
        ++++ <&script> pa004_traceback_test012.py
        ++++ <&script> pa004_traceback_test013.py
        ++++ <&script> pa004_traceback_test014.py
        ++++ <&script> pa004_traceback_test015.py
        ++ <&folder> UML
        +++ <&folder> exceptions_py
        ++++ <&code> ConstantAssignment.iuml
        ++++ <&code> Custom Exception Instantiation.pu
        ++++ <&image> Custom_Exception_Instantiation.png
        ++++ <&code> CustomAttributeError.iuml
        ++++ <&code> CustomError._ _subclasshook_ _() Activity.pu
        ++++ <&image> CustomError._ _subclasshook_ _()_Activity.png
        ++++ <&code> CustomError.iuml
        ++++ <&code> CustomTypeError.iuml
        ++++ <&code> CustomValueError.iuml
        ++++ <&code> ErrorMixin._ _del_ _() Activity.pu
        ++++ <&image> ErrorMixin._ _del_ _()_Activity.png
        ++++ <&code> ErrorMixin.iuml
        ++++ <&code> ErrorMixin.presetTraceback() Activity.pu
        ++++ <&image> ErrorMixin.presetTraceback()_Activity.png
        ++++ <&code> ErrorMixin.Traceback Activity.pu
        ++++ <&image> ErrorMixin.Traceback_Activity.png
        ++++ <&code> exceptions Class Diagram (Direct Only).pu
        ++++ <&code> exceptions Class Diagram.pu
        ++++ <&image> exceptions_Class_Diagram_(Direct_Only).png
        ++++ <&image> exceptions_Class_Diagram.png
        ++++ <&code> exceptions_Components.iuml
        ++++ <&code> NotInDCError.iuml
        +++ <&folder> Miscellaneous
        ++++ <&code> Custom Exceptions tree.pu
        ++++ <&image> Custom_Exceptions_tree.png
        ++++ <&code> Exceptions tree.pu
        ++++ <&image> Exceptions_tree.png
        +++ <&folder> Templates
        ++++ <&code> Classes.cuml
        ++++ <&code> Components.cuml
        +++ <&folder> utils
        ++++ <&folder> contracts_py
        +++++ <&code> contracts.py Use Cases.pu
        +++++ <&image> contracts.py_Use_Cases.png
        ++++ <&folder> docstring_parsers_py
        +++++ <&code> AAParser.extractArguments() Activity.pu
        +++++ <&image> AAParser.extractArguments()_Activity.png
        +++++ <&code> AAParser.iuml
        +++++ <&code> docstring_parsers Classes.pu
        +++++ <&code> docstring_parsers Use Cases.pu
        +++++ <&image> docstring_parsers_Classes.png
        +++++ <&image> docstring_parsers_Use_Cases.png
        +++++ <&code> EpytextParser.iuml
        +++++ <&code> GenericParser.extractArguments() Activity.pu
        +++++ <&image> GenericParser.extractArguments()_Activity.png
        +++++ <&code> GenericParser.extractLinesByTokens() Activity.pu
        +++++ <&image> GenericParser.extractLinesByTokens()_Activity.png
        +++++ <&code> GenericParser.extractRaises() Activity.pu
        +++++ <&image> GenericParser.extractRaises()_Activity.png
        +++++ <&code> GenericParser.extractReturnedValues() Activity.pu
        +++++ <&image> GenericParser.extractReturnedValues()_Activity.png
        +++++ <&code> GenericParser.extractSignature() Activity.pu
        +++++ <&image> GenericParser.extractSignature()_Activity.png
        +++++ <&code> GenericParser.iuml
        +++++ <&code> GenericParser.reduceDocstring() Activity.pu
        +++++ <&image> GenericParser.reduceDocstring()_Activity.png
        +++++ <&code> GenericParser.trimDocstring() Activity.pu
        +++++ <&image> GenericParser.trimDocstring()_Activity.png
        +++++ <&code> GoogleParser.iuml
        +++++ <&code> indent_docstring() Activity.pu
        +++++ <&image> indent_docstring()_Activity.png
        +++++ <&code> NumPydocParser.extractRaises() Activity.pu
        +++++ <&image> NumPydocParser.extractRaises()_Activity.png
        +++++ <&code> NumPydocParser.extractReturnedValues() Activity.pu
        +++++ <&image> NumPydocParser.extractReturnedValues()_Activity.png
        +++++ <&code> NumPydocParser.iuml
        +++++ <&code> reSTParser.extractSignature() Activity.pu
        +++++ <&image> reSTParser.extractSignature()_Activity.png
        +++++ <&code> reSTParser.iuml
        ++++ <&folder> dynamic_import_py
        +++++ <&code> import_from_module() Activity.pu
        +++++ <&image> import_from_module()_Activity.png
        +++++ <&code> import_module() Activity.pu
        +++++ <&image> import_module()_Activity.png
        ++++ <&folder> loggers_py
        +++++ <&code> ConsoleLogger Initialization Activity.pu
        +++++ <&image> ConsoleLogger_Initialization_Activity.png
        +++++ <&code> ConsoleLogger._ _getattribute_ _() Activity.pu
        +++++ <&image> ConsoleLogger._ _getattribute_ _()_Activity.png
        +++++ <&code> ConsoleLogger._ _setattr_ _() Activity.pu
        +++++ <&image> ConsoleLogger._ _setattr_ _()_Activity.png
        +++++ <&code> ConsoleLogger.enableConsoleLogging() Activity.pu
        +++++ <&image> ConsoleLogger.enableConsoleLogging()_Activity.png
        +++++ <&code> ConsoleLogger.iuml
        +++++ <&code> DualLogger Initialization Activity.pu
        +++++ <&image> DualLogger_Initialization_Activity.png
        +++++ <&code> DualLogger.changeLogFile() Activity.pu
        +++++ <&image> DualLogger.changeLogFile()_Activity.png
        +++++ <&code> DualLogger.enableFileLogging() Activity.pu
        +++++ <&image> DualLogger.enableFileLogging()_Activity.png
        +++++ <&code> DualLogger.iuml
        +++++ <&code> loggers.py Class Diagram.pu
        +++++ <&image> loggers.py_Class_Diagram.png
        ++++ <&folder> traceback_py
        +++++ <&code> ExceptionTraceback._ _init_ _() Activity.pu
        +++++ <&image> ExceptionTraceback._ _init_ _()_Activity.png
        +++++ <&code> ExceptionTraceback.iuml
        +++++ <&code> StackTraceback._ _del_ _() Activity.pu
        +++++ <&image> StackTraceback._ _del_ _()_Activity.png
        +++++ <&code> StackTraceback._ _init_ _() Activity.pu
        +++++ <&image> StackTraceback._ _init_ _()_Activity.png
        +++++ <&code> StackTraceback.CallChain Property Activity.pu
        +++++ <&image> StackTraceback.CallChain_Property_Activity.png
        +++++ <&code> StackTraceback.Info Property Activity.pu
        +++++ <&image> StackTraceback.Info_Property_Activity.png
        +++++ <&code> StackTraceback.iuml
        +++++ <&code> traceback Classes.pu
        +++++ <&image> traceback_Classes.png
        ++++ <&code> utils Components.pu
        ++++ <&code> utils_components.iuml
        ++++ <&image> utils_Components.png
        +++ <&code> pos Components.pu
        +++ <&image> pos_Components.png
        ++ <&folder> User_Documentation
        +++ <&document> UD001 Module pos.utils.traceback Reference.odt
        +++ <&document> UD002 Module pos.exceptions Reference.odt
        +++ <&document> UD003 Module pos.utils.docstring_parsers Reference.odt
        +++ <&document> UD004 Module pos.utils.dynamic_import Reference.odt
        +++ <&document> UD005 Module pos.utils.loggers Reference.odt
        + <&folder> Tests
        ++ <&folder> utils
        +++ <&script> _ _init_ _.py
        +++ <&script> docstring_parsers_ut.py
        +++ <&script> traceback_ut.py
        +++ <&script> utils_all_ut.py
        ++ <&script> _ _init_ _.py
        ++ <&script> base_classes_descriptedabc_ut.py
        ++ <&script> exceptions_ut.py
        ++ <&script> pos_all_ut.py
        + <&folder> utils
        ++ <&script> _ _init_ _.py
        ++ <&script> attr_info.py
        ++ <&script> docstring_parsers.py
        ++ <&script> dynamic_import.py
        ++ <&script> loggers.py
        ++ <&script> traceback.py
        + <&script> _ _init_ _.py
        + <&script> base_classes.py
        + <&script> exceptions.py
        + <&info> pos File Structure.md
        + <&info> README.md
        + <&info> Release log.md
    }
}

@enduml
```