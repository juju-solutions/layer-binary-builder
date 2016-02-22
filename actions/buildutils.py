import os
import shutil
import hashlib
from git import Repo, Git
from subprocess import check_call
import json
import apt
from charmhelpers.core import hookenv

class BuildHelper:
    
    def __init__(self, target_name, final_filename_template):
        self.workspace = "/tmp/workspace"
        self.target_name = target_name
        self.final_filename_template = final_filename_template
        self.source_path =  os.path.join(self.workspace, self.target_name)


    def add_apt_repository(self, repository):        
        check_call(['apt-add-repository', repository])


    def install_apt_packages(self, package_names):
        cache = apt.cache.Cache()
        cache.update()
    
        for package_name in package_names:
            pkg = cache[package_name]
    
            hookenv.log("Installing {pkg_name}".format(pkg_name=package_name))
            if pkg.is_installed:
                hookenv.log("{pkg_name} already installed".format(pkg_name=package_name))
            else:
                pkg.mark_install()
    
        cache.commit()

        
    def checkout_source(self, git_path, checkout_options = None):
        '''
        Checkout source and switch to the right tag
        '''
        shutil.rmtree(self.workspace, ignore_errors=True)
        os.mkdir(self.workspace)
        os.chdir(self.workspace)
        Repo.clone_from(git_path, self.target_name)
        g = Git(self.source_path)
        g.checkout(checkout_options)    


    def build_binary(self, command):
        os.chdir(self.source_path)
        check_call(command)


    def set_output_file(self, produced_file):
        digest = self.get_hash(produced_file)    
        output_filename = self.get_filename(digest)
        os.renames(produced_file, output_filename)
        self.store_metadata(digest)
        return digest, os.path.join(self.workspace, output_filename)


    def store_metadata(self, digest):
        '''
        Storing metadata for the build. Note that we overwrite the metadata file every time we build.  
        '''
        outputfilename = self.get_filename(digest)    
        metadata = {'FileName' : outputfilename,
                    'Workspace' : self.workspace}
        with open(os.path.join(self.workspace, ".metadata"), 'w') as f:
            json.dump(metadata, f)

    
    def get_hash(self, file_name):
        '''
        Get the sha 256 digest
        '''
        with open(file_name, 'rb') as f:
            m = hashlib.sha256()
            m.update(f.read())
            res = m.hexdigest()
        return res
    
    
    def get_filename(self, digest):
        outputfilename = self.final_filename_template.format(digest[:7])    
        return outputfilename
