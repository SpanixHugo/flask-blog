from blog import create_blog

# __name__ changes to __main__ whenever the file is running
if __name__ == "__main__":
    blog = create_blog()
    blog.run(debug=True, port = 5000) # For Development purpose