from pd2.input.parser import DocParser

filenames = [
        "xml/0.xml",
        "xml/1.xml",
        "xml/2.xml",
        "xml/0.xml",
        "xml/1.xml",
        "xml/2.xml",
        "xml/0.xml",
        "xml/1.xml",
        "xml/2.xml",
]

old = ()

parser = DocParser(old)
parser.read_documents(filenames)
[print(x) for x in parser.games]
[print(x) for x in parser.teams]
[print(x) for x in parser.players]
[print(x) for x in parser.goals]
[print(x) for x in parser.penalties]
[print(x) for x in parser.referees]

