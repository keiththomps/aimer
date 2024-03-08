import argparse

def main():
    parser = argparse.ArgumentParser(prog='ghost', description='Ghost Writer Command Line Utility')
    
    parser.add_argument('-p', '--prompt', type=str, required=True, 
                        help='Specifies the prompt to use in non-interactive mode. A path or a url can also be specified - in this case the content at the specified path or url is used as the prompt. The prompt can leverage the liquidjs templating system.')
    
    parser.add_argument('-a', '--ai', type=str, default='OpenAI', 
                        help='AI service to use, defaults to OpenAI, but allows for anthropic')
    
    parser.add_argument('-m', '--model', type=str, default='gpt-4-turbo-preview', 
                        help='Optional flag to set the model, defaults to gpt-4-turbo-preview. Using the value "gpt3" will use the gpt-3.5-turbo model.')
    
    parser.add_argument('-d', '--dry-run', action='store_true', 
                        help='Optional boolean flag that can be used to run the tool in dry-run mode where only the prompt that will be sent to the model is displayed. No changes are made to your filesystem when this option is used.')
    
    parser.add_argument('-i', '--interactive', action='store_true', 
                        help='Optional boolean flag that enables interactive mode where the user can provide input interactively. If this flag is not set, the tool runs in non-interactive mode.')
    
    parser.add_argument('-t', '--template', type=str, nargs=2, metavar=('templateName', 'templatePath'), 
                        help='Optional flag to set the template name and path.')
    
    parser.add_argument('-x', action='store_true', 
                        help='Optional boolean flag. Ghost parses the model\'s response and applies the resulting operations to your file system when using the default template. You only need to pass the -x flag if you\'ve created your own template, and you want Ghost to parse and apply the output in the same way that the built in "refactor" template output is parsed and applied to your file system.')
    
    parser.add_argument('-o', '--output-path', type=str, 
                        help='Optional string flag that specifies the path to the output file. If this flag is not set, the output will be printed to stdout.')
    
    parser.add_argument('files', nargs='*', help='Files to process')
    
    args = parser.parse_args()
    
    # TODO: Implement the functionality of the command using the arguments in 

if __name__ == '__main__':
    main()
