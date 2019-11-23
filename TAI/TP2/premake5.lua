workspace "tp1"
    architecture "x64"
    configurations { "debug", "release" }

folder = "%{cfg.buildcfg}/%{cfg.system}/%{cfg.architecture}"

project "wav"
    location "config/%{prj.name}"
    kind "StaticLib"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"

    targetdir ("bin/%{prj.name}")
    objdir ("int/%{prj.name}")

    links
    {
        "sndfile"
    }

    files
    {
        "src/%{prj.name}/**.cpp",
        "include/%{prj.name}/**.hpp"
    }

    includedirs
    {
        "include"
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

project "wavcb"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"

    targetdir ("bin/")
    objdir ("int/")

    files
    {
        "src/%{prj.name}.cpp",
        "include/**.hpp"
    }

    includedirs
    {
        "include"
    }

    links
    {
        "wav",
        "sndfile",
        "pthread"
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

project "wavcmp"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/")
    objdir ("int/")
    
    files
    {
        "src/%{prj.name}.cpp",
        "include/**.hpp"
    }
    
    includedirs
    {
        "include"
    }
    
    links
    {
        "wav",
        "sndfile"
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

project "wavcp"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/")
    objdir ("int/")
    
    files
    {
        "src/%{prj.name}.cpp",
        "include/**.hpp"
    }
    
    includedirs
    {
        "include"
    }
    
    links
    {
        "wav",
        "sndfile"
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

project "wavfind"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/")
    objdir ("int/")
    
    files
    {
        "src/%{prj.name}.cpp",
        "include/**.hpp"
    }
    
    includedirs
    {
        "include"
    }
    
    links
    {
        "wav",
        "sndfile"
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

project "wavhist"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/")
    objdir ("int/")
    
    files
    {
        "src/%{prj.name}.cpp",
        "include/**.hpp"
    }
    
    includedirs
    {
        "include"
    }
    
    links
    {
        "wav",
        "sndfile"
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

project "wavquant"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/")
    objdir ("int/")
    
    files
    {
        "src/%{prj.name}.cpp",
        "include/**.hpp"
    }
    
    includedirs
    {
        "include"
    }
    
    links
    {
        "wav",
        "sndfile"
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