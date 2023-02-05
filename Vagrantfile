Vagrant.configure("2") do |config|
	config.vm.define "alpine" do |alpine|
		# config.vm.network "forwarded_port", guest: 80, host: 8180
		# config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__args: ["--verbose", "--archive", "--delete", "-z"]
		alpine.vm.synced_folder ".", "/vagrant", SharedFoldersEnableSymlinksCreate: true
		# alpine.vm.synced_folder "./home", "/home/vagrant", owner: "vagrant",
		  # group: "vagrant", SharedFoldersEnableSymlinksCreate: true
    # https://stackoverflow.com/a/39759154
		# alpine.vm.network "public_network", ip: "192.168.1.250"
		alpine.vm.box = "boxomatic/alpine-3.17"
		alpine.vm.box_version = "20221221.0.1"
		alpine.vm.box_check_update = false
		alpine.vm.provider "virtualbox" do |vb|
			vb.gui = false
			vb.memory = "1024"
		    # https://sourcegraph.com/github.com/mastodon/mastodon/-/blob/Vagrantfile?L110&subtree=true
		    # Disable VirtualBox DNS proxy to skip long-delay IPv6 resolutions.
		    # https://github.com/mitchellh/vagrant/issues/1172
		    # public_ip		-> 15m20s
		    # on, virtio	-> 6m45s
		    # off, virtio	-> 6m28s
		    # comment, virt -> 6m24s
		    # nothing       -> 6m10s
		    # vb.customize ["modifyvm", :id, "--natdnsproxy1", "off"]
		    # vb.customize ["modifyvm", :id, "--natdnshostresolver1", "off"]

		    # Use "virtio" network interfaces for better performance.
		    # vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
		    # vb.customize ["modifyvm", :id, "--nictype2", "virtio"]
		end
        alpine.vm.provision 'bootstrap', type: 'shell' do |s|
            s.inline = 'sudo apk update;'\
                       'sudo apk upgrade;'\
                       'sudo apk add sshpass;'\
                       'ssh-keyscan -H 192.168.1.3 >> /home/vagrant/.ssh/known_hosts;'\
                       'ssh-keyscan -H localhost   >> /home/vagrant/.ssh/known_hosts;'\
                       'ssh-keyscan -H 127.0.0.1   >> /home/vagrant/.ssh/known_hosts;'
        end
		alpine.vm.provision "ansible_local" do |ansible|
			ansible.verbose = "v"
			ansible.config_file = "ansible.cfg.ini"
			ansible.inventory_path = "inventory.ini"
			ansible.limit = "localhost"
			ansible.playbook = "alpine.yml"
		end
	end
end
