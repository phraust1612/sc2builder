<div align="center">
    <a href="https://www.youtube.com/watch?v=ihJu7IURpAk" target="_blank">
        <img src="https://img.youtube.com/vi/ihJu7IURpAk/0.jpg" width="480" height="360" border="10">
    </a>
</div>

# Sc2Builder

17.ver 1.0 released

## About

[Sc2Builder](https://github.com/phraust1612/sc2builder) is [Min Byeonguk](https://github.com/phraust1612)'s build-order calculator of [Starcraft II - Legacy of the Void](https://starcraft2.com) in GUI. It gives you a demonstration of Starcraft II in a graph, so you can easily check resource, units, buildings or etc before you play real Starcraft II. Through Sc2Builder, you can optimize your old build-order, or you can make a new one. Sc2Builder provides save and load build-orders, so you can share your proud build-order on social medias.


If you want to report some bugs, please contact me via phraust1612@gmail.com

## Assumption

+ Game speed is 'faster' in Starcraft II.
+ Each expansion has 8 mineral fields and 2 vespin gas layers.
+ Sc2Builder doesn't support gold mineral fields.
+ For each mineral field and gas layer, at most 2 and 3 workers can work on it.
+ Depletion of mineral fields and gas layers will not be applied.
+ Maximum game time is 2hrs 46mins 40secs and Sc2Builder will not support later than it.

## How to Use

### git

You can install Sc2Builder with git :

```shell
$ git clone https://github.com/phraust1612/sc2builder.git
$ python3 sc2builder/Sc2Builder protoss
'''

You can pass your race via command line, but it's not necessary.
If sys gets no argv about race, it will automatically bring protoss.

### zip files

You can also directly download zip files that matches to your OS.
Unzip it and execute 'Sc2Builder.exe'
