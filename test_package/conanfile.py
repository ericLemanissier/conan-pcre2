#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        if self.settings.os == "Windows" and not self.options['pcre2'].shared:
            cmake.definitions['PCRE2_STATIC'] = True
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "test_package")
            arguments = "%sw+ Bincrafters" % ("\\" if self.settings.os == "Windows" else "\\\\")
            if self.settings.os == "Windows":
                self.run("%s %s" % (bin_path, arguments))
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path, arguments))
            else:
                self.run("LD_LIBRARY_PATH=%s %s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path, arguments))
