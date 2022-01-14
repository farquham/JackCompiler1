# Compiler for Jack programming language, for Nand to Tetris wk10
import sys
import re

# Jack code file -> XML file with identifiers
# Initializes and uses Tokenizer and Parser Objects
def main():
    # Intializes the parser object
    jfile = sys.argv[1]

    # makes tokenizer list to hold final tokens
    tokens = []

    t = Tokenizer(jfile)
    while t.hasMoreTokens() == True:
        TT = t.tokenType()
        if (main_helper(TT,t) == None):
            t.advance()
        else:
            tokens.append([main_helper(TT,t), TT.lower()])
            t.advance()
    if (main_helper(t.tokenType(),t) == None):
        print("ignore")
    else:
        tokens.append([main_helper(t.tokenType(),t), TT.lower()])

    #tfilename = ((jfile.split(".")[0]) +"TC.xml")
    #tfiles = open(tfilename, "w")
    #for x in range(0,len(tokens)):
    #    tfiles.write((tokens[x][0])+"\n")
    #tfiles.close()

    c = CompEngine(sys.argv[1],tokens)
    c.compileClass()

    c.Close()

# Simplifies the main function, may not be needed
def main_helper(TT,t):
    if TT == "KEYWORD":
        return (t.keyWord())
    elif TT == "SYMBOL":
        return (t.symbol())
    elif TT == "IDENTIFIER":
        return (t.indentifier())
    elif TT == "INT_CONST":
        return (t.intVal())
    elif TT == "STRING_CONST":
        return (t.stringVal())
    else:
        return

def filtfunc(x):
    if (x == " ") or (x == ""):
        return False
    else:
        return True


# Breaks down the input file and outputs a stream of individual tokens which
# are classified into lexical categories
class Tokenizer:
    # opens input .jack file and gets ready to tokenize it
    def __init__(self,filearg):
        file = open(filearg, "r")
        self.lines = file.readlines()
        file.close()
        self.lcounter = 0
        self.line = (self.lines)[self.lcounter]
        self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n)", self.line)))
        self.tcounter = 0
        self.token = (self.line)[self.tcounter]


    # checks if there are more tokens in the input file
    def hasMoreTokens(self):
        if (self.lcounter == (len(self.lines)-1)):
            if (self.tcounter == (len(self.line)-1)):
                return False
            else:
                return True
        else:
            return True

    # gets next token from input and makes it current token
    def advance(self):
        if (self.token == "//") or (self.token == "/**") or (re.match(r"\/\w*",self.token)):
            self.lcounter += 1
            self.line = (self.lines)[self.lcounter]
            self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n)",self.line)))
            self.tcounter = 0
            self.token = (self.line)[self.tcounter]
        elif (self.tcounter == (len(self.line)-1)):
            self.lcounter += 1
            self.line = (self.lines)[self.lcounter]
            self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n)",self.line)))
            self.tcounter = 0
            self.token = (self.line)[self.tcounter]
        else:
            self.tcounter += 1
            self.token = (self.line)[self.tcounter]

    # Returns the type of the current token as a constant
    def tokenType(self):
        lexEle = {"class":"KEYWORD","constructor":"KEYWORD","function":"KEYWORD",
                  "method":"KEYWORD","field":"KEYWORD","static":"KEYWORD","var":"KEYWORD",
                  "int":"KEYWORD","char":"KEYWORD","boolean":"KEYWORD","void":"KEYWORD",
                  "true":"KEYWORD","false":"KEYWORD","null":"KEYWORD","this":"KEYWORD",
                  "let":"KEYWORD","do":"KEYWORD","if":"KEYWORD","else":"KEYWORD"
                  ,"while":"KEYWORD","return":"KEYWORD","{":"SYMBOL","}":"SYMBOL",
                  "(":"SYMBOL",")":"SYMBOL","[":"SYMBOL","]":"SYMBOL",".":"SYMBOL",
                  ",":"SYMBOL",";":"SYMBOL","+":"SYMBOL","-":"SYMBOL","*":"SYMBOL",
                  "/":"SYMBOL","&":"SYMBOL","|":"SYMBOL","<":"SYMBOL",">":"SYMBOL",
                  "=":"SYMBOL","~":"SYMBOL",}
        if (self.token == "//") or (self.token == "/**") or (self.token == "") or (self.token == "\n") or (re.match(r"\/\w*",self.token)):
            return ""
        try:
            return lexEle[self.token]
        except:
            if (re.match('\d+',self.token)):
                return "INT_CONST"
            elif (re.match('^([A-Z]|[a-z])\w*',self.token)):
                return "IDENTIFIER"
            else:
                return "STRING_CONST"

    # Returns the keyword associated with the current token
    def keyWord(self):
       # kWords = {"class":"CLASS","constructor":"CONSTRUCTOR","function":"FUNCTION",
       #           "method":"METHOD","field":"FIELD","static":"STATIC","var":"VAR",
       #           "int":"INT","char":"CHAR","boolean":"BOOLEAN","void":"VOID",
       #           "true":"TRUE","false":"FALSE","null":"NULL","this":"THIS",
       #           "let":"LET","do":"DO","if":"IF","else":"ELSE"
       #           ,"while":"WHILE","return":"RETURN"}
        return self.token

    # Returns the character which is the current token
    def symbol(self):
        symd = {"<":"&lt",">":"&gt","&":"&amp"}
        if (self.token in ["<",">","&"]):
            return symd[self.token]
        else:
            return self.token

    # Returns the indentifier which is the current token
    def indentifier(self):
        return self.token

    # Returns the int value of the current token
    def intVal(self):
        return int(self.token)

    # Returns the string value of the current token (without enclosing double
    # quotes)
    def stringVal(self):
        return (self.token).strip("\"")




# Takes the list of individual tokens and compiles a XML output file that
# creates a token tree with indentifiers
class CompEngine:
    # Creates new comp engine with given input and output files
    def __init__(self,filename,tokens):
        nfilename = ((filename.split(".")[0]) +".xml")
        print(nfilename)
        self.newfile = open(nfilename, "w")
        self.count = 0
        self.tokens = tokens

    # Compiles a complete class
    def compileClass(self):
        self.newfile.write("<class>\n")
        while (self.tokens[(self.count)][1] != "symbol"):
            self.newfile.write("<"+(self.tokens[self.count][1])+"> " + (self.tokens[self.count][0]) + " </"+(self.tokens[self.count][1])+">\n")
            self.count += 1
        self.newfile.write("<"+(self.tokens[self.count][1])+"> " + (self.tokens[self.count][0]) + " </"+(self.tokens[self.count][1])+">\n")
        self.count += 1
        while ((self.count) < (len(self.tokens)-1)):
            #print(self.tokens[self.count][0] + self.tokens[self.count][1] +  str(self.count))
            if (self.tokens[self.count][0] in ["static","field"]):
                self.compileClassVarDec()
            if (self.tokens[self.count][0] in ["function","method","constructor"]):
                self.compileSubroutineDec()
            if (self.tokens[self.count][0] == "{"):
                self.compileSubroutineBody()
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        self.newfile.write("</class>")

    # Compiles a stateic variable declaration or field declaration
    def compileClassVarDec(self):
        self.newfile.write("<classVarDec>\n")
        while (self.tokens[(self.count)][0] != ";"):
              self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
              self.count += 1
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        self.newfile.write("</classVarDec>\n")
        return

    # Compiles a complete method, funciton, or constructor
    def compileSubroutineDec(self):
        self.newfile.write("<subroutineDec>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        while (self.tokens[self.count][1] != "symbol"):
            #print(self.tokens[self.count][0] + "," + self.tokens[self.count][1] + "," + str(self.count))
            self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
            self.count += 1
        if (self.tokens[self.count][0] == "("):
            self.compileParameterList()
        if (self.tokens[self.count][0] == "{"):
            self.compileSubroutineBody()
        self.newfile.write("</subroutineDec>\n")
        return

    # Compiles a (maybe empty) paramter list (ignores enclosing ())
    def compileParameterList(self):
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        self.newfile.write("<parameterList>\n")
        while (self.tokens[self.count][0] != ")"):
            self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
            self.count += 1
        self.newfile.write("</parameterList>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # Compiles a subroutine's body
    def compileSubroutineBody(self):
        self.newfile.write("<subroutineBody>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        while (self.tokens[(self.count)][0] != "}"):
            #print(self.tokens[self.count][0] + self.tokens[self.count][1] + str(self.count))
            if (self.tokens[self.count][0] == "var"):
                self.compileVarDec()
            if (self.tokens[self.count][0] in ["let","if","while","do","return"]):
                self.compileStatements()
            if (self.tokens[(self.count)][0] in ["method","constructor","function"]):
                    break
        self.newfile.write("</subroutineBody>\n")
        return

    # Compiles a var declaration
    def compileVarDec(self):
        self.newfile.write("<varDec>\n")
        while (self.tokens[(self.count)-1][0] != ";") or (self.tokens[self.count][0] == "var"):
              self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
              self.count += 1
        self.newfile.write("</varDec>\n")
        return

    # Compiles a sequence of statements (ignores enclosing {})
    def compileStatements(self):
        self.newfile.write("<statements>\n")
        while (self.tokens[self.count][0] != "}"):
            print(self.tokens[self.count][0] + self.tokens[self.count][1] +  str(self.count))
            if (self.tokens[self.count][0] == "let"):
                print("LET")
                self.compileLet()
            if (self.tokens[self.count][0] == "if"):
                print("IF")
                self.compileIf()
            elif (self.tokens[self.count][0] == "while"):
                print("WHILE")
                self.compileWhile()
            elif (self.tokens[self.count][0] == "do"):
                print("DO")
                self.compileDo()
            elif (self.tokens[self.count][0] == "return"):
                print("RETURN")
                self.compileReturn()
        self.newfile.write("</statements>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # Compiles a let statement
    def compileLet(self):
        self.newfile.write("<letStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != ";") or (self.tokens[(self.count)][0] == "let")) and (src < 1):
            if (self.tokens[self.count][0] != "="):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                src += 1
        self.newfile.write("</letStatement>\n")
        return

    # Compiles an if statement (matbe with trailing else)
    def compileIf(self):
        self.newfile.write("<ifStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != "}") or (self.tokens[self.count][0] == "if")) and (src < 1):
            if (self.tokens[self.count][0] != ("(" or "{")):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
            elif (self.tokens[self.count][0] == "("):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
            if (self.tokens[self.count][0] == "{"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileStatements()
                src += 1
        if (self.tokens[self.count][0] == "else"):
            while (self.tokens[(self.count)-1][0] != "}"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                if (self.tokens[self.count][0] == "{"):
                     self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                     self.count += 1
                     self.compileStatements()
        self.newfile.write("</ifStatement>\n")
        return

    # Compiles a while statement
    def compileWhile(self):
        self.newfile.write("<whileStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != "}") or (self.tokens[(self.count)][0] == "while")) and (src < 1):
             if (self.tokens[self.count][0] != ("(" or "{")):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
             elif (self.tokens[self.count][0] == "("):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                print("while check")
             if (self.tokens[self.count][0] == "{"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileStatements()
                src += 1
        self.newfile.write("</whileStatement>\n")
        return

    # Compiles a do statement
    def compileDo(self):
        self.newfile.write("<doStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != ";") or (self.tokens[(self.count)][0] == "do")) and (src < 1):
            if (self.tokens[self.count][0] != "("):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpressionList()
                src += 1
        self.newfile.write("</doStatement>\n")
        return

    # Compiles a return statement
    def compileReturn(self):
        self.newfile.write("<returnStatement>\n")
        src = 0
        while (self.tokens[(self.count)-1][0] != ";") or (self.tokens[(self.count)][0] == "return"):
             if (self.tokens[self.count][1] == "identifier"):
                 self.compileExpression()
             else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</returnStatement>\n")
        return

    # Compiles an expression
    def compileExpression(self):
        self.newfile.write("<expression>\n")
        self.compileTerm()
        self.newfile.write("</expression>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # Compiles a term (will likelu need to lookahead 1 token to distinguish
    # between possiblilities
    def compileTerm(self):
        self.newfile.write("<term>\n")
        while (self.tokens[(self.count)][0] != ";"):
            print(self.tokens[self.count][0])
            if (self.tokens[(self.count)+1][0] == "[") and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                break
            elif (self.tokens[(self.count)+1][0] == "(") and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpressionList()
                print("Term check")
                break
            elif (self.tokens[(self.count)+1][0] == ".") and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</term>\n")
        return

    # Compiles a (maybe empty) comma-separated list of expressions
    def compileExpressionList(self):
        self.newfile.write("<expressionList>\n")
        while (self.tokens[(self.count)-1][0] != ")"):
            print(str(self.count))
            if (self.tokens[(self.count)][1] in ["identifier","keyword"]):
                self.compileExpression()
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</expressionList>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # closes the output file
    def Close(self):
        self.newfile.close()

# Starts the program
if __name__== "__main__":
    main()
