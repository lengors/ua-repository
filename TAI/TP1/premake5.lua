workspace "tp1"
    architecture "x64"
    configurations { "debug", "release" }

folder = "%{cfg.buildcfg}/%{cfg.system}/%{cfg.architecture}"

project "markov_model"
    location "config/%{prj.name}"
    kind "StaticLib"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/" .. folder .. "/%{prj.name}")
    objdir ("int/" .. folder .. "/%{prj.name}")

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

    filter "configurations:debug"
        runtime "Debug"
        symbols "on"

    filter "configurations:release"
        runtime "Release"
        optimize "on"

project "fcm"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/" .. folder .. "/%{prj.name}")
    objdir ("int/" .. folder .. "/%{prj.name}")

    files
    {
        "src/%{prj.name}/**.cpp"
    }

    includedirs
    {
        "include"
    }

    links
    {
        "markov_model"
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

project "fcm"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/" .. folder .. "/%{prj.name}")
    objdir ("int/" .. folder .. "/%{prj.name}")

    files
    {
        "src/%{prj.name}/**.cpp",
        "include/%{prj.name}/**.hpp"
    }

    includedirs
    {
        "include"
    }

    links
    {
        "markov_model"
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

project "generator"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"

    targetdir ("bin/" .. folder .. "/%{prj.name}")
    objdir ("int/" .. folder .. "/%{prj.name}")

    files
    {
        "src/%{prj.name}/**.cpp"
    }

    includedirs
    {
        "include"
    }

    links
    {
        "markov_model"
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

project "comparator"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
    
    targetdir ("bin/" .. folder .. "/%{prj.name}")
    objdir ("int/" .. folder .. "/%{prj.name}")
    
    files
    {
        "src/%{prj.name}/**.cpp"
    }
    
    includedirs
    {
        "include"
    }
    
    links
    {
        "markov_model"
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

project "analyzer"
    location "config/%{prj.name}"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    staticruntime "on"
        
    targetdir ("bin/" .. folder .. "/%{prj.name}")
    objdir ("int/" .. folder .. "/%{prj.name}")
        
    files
    {
        "src/%{prj.name}/**.cpp"
    }
        
    includedirs
    {
        "include"
    }
        
    links
    {
        "markov_model"
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