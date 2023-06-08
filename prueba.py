from rich import print

from kultimate.utils import ParserMarkdown

if __name__ == "__main__":
    parser = ParserMarkdown("/home/felipe/Dropbox/kanban2/todo.md")
    print(parser.get_tasks())
    # print(parser.pretty())
