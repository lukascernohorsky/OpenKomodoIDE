# Minimal configuration for testing
import os

# Configuration variables
platform = "linux"
mozVer = 140.0
komodoVersion = "12.0"
buildDir = os.path.abspath("build")
srcTreeName = "moz14000-ko12.0"
buildType = "release"
enableDebug = False
enableSymbols = True
mozSrcType = "hg"
mozSrcHgRepo = "14000"
mozSrcHgTag = None

# Print configuration for verification
print("Test configuration created:")
print(f"  platform: {platform}")
print(f"  mozVer: {mozVer}")
print(f"  komodoVersion: {komodoVersion}")
print(f"  buildDir: {buildDir}")
print(f"  srcTreeName: {srcTreeName}")