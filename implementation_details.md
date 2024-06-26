# To ignore big files when adding the files to tracking stage use
```
find . -size +1G | cat >> .gitignore
```

# To ignore files or folder just add it to 
>.gitignore

# To clone or push by acces token
> https://stackoverflow.com/questions/18935539/authenticate-with-github-using-a-token

# How to store you PAT globaly in GIT so you are not supposed to type it every time you intend to clone or push a repo: 
> https://stackoverflow.com/questions/46645843/where-to-store-my-git-personal-access-token

# To create an entrypoint.sh
> Create your file then make it excutable 
```
chmod +x entrypoint.sh
```
> You can now run the project from this file by running the file directly from its path
```
./entrypoint.sh
```