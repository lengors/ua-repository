workspace "tp1"
    architecture "x64"
    configurations { "debug", "release" }



project "main"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++11"
    staticruntime "on"

    targetdir ("bin/")
    objdir ("int/")

    files
    {
        "src/%{prj.name}.cpp",
        
    }

    includedirs
    {
        "include"
    }

    links
    {
        "NCCD",
        "NCD",
        "opencv_core",
        "opencv_imgcodecs",
        "opencv_imgproc",
        "opencv_highgui"
        
    }

    filter "system:windows"
        systemversion "latest"

    filter "system:linux"
        systemversion "latest"

    filter "system:macosx"
        systemversion "latest"

    filter "configurations:debug"
        runtime "Debug"
        symbols "on"

    filter "configurations:release"
        runtime "Release"
        optimize "on"

project "NCD"
    kind "StaticLib"
    language "C++"
    files{
        "src/NCD.hpp",
        "src/NCD.cpp"

    }
project "resize"
    kind "ConsoleApp"
    language "C++"
    files{
        "src/resize.cpp"
    }
    links{
        "opencv_core",
        "opencv_imgcodecs",
        "opencv_imgproc",
        "opencv_highgui"

    }
project "test"
    kind "ConsoleApp"
    language "C++"
    files{
        "src/test.cpp"
    }
    
project "NCCD"
    kind "StaticLib"
    language "C++"
    files{
        "src/NCCD.hpp",
        "src/NCCD.cpp"

    }
    links{
        "opencv_core",
        "opencv_highgui"
    }