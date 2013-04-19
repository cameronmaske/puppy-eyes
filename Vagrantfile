Vagrant::Config.run do |config|
    config.vm.define :trackmaven do |config|
        config.vm.box = "puppy-eyes"
        config.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-server-1204-x64.box"
        config.vm.forward_port 8001, 8000

        #Enable puppet
        config.vm.provision :puppet do |puppet|
            puppet.module_path = "vagrant/puppet/modules"
            puppet.manifests_path = "vagrant/puppet/manifests"
            puppet.manifest_file  = "default.pp"
            puppet.options = [
                '--verbose',
                '--debug',
            ]
        end
        config.vm.share_folder "puppy-eyes", "/home/vagrant/puppy-eyes", "."
    end
end