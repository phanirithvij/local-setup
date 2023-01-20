Vagrant.configure("2") do |config|
	config.vm.define "alpine" do |alpine|
		# config.vm.network "forwarded_port", guest: 80, host: 8180
		# config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__args: ["--verbose", "--archive", "--delete", "-z"]
		config.vm.synced_folder ".", "/vagrant"
		alpine.vm.box = "boxomatic/alpine-3.17"
		alpine.vm.box_version = "20221221.0.1"
		alpine.vm.box_check_update = false
		alpine.vm.provider "virtualbox" do |vb|
			vb.gui = false
			vb.memory = "1024"
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
			ansible.config_file = "ansible.cfg"
			ansible.inventory_path = "inventory"
			ansible.limit = "localhost"
			ansible.playbook = "main.yml"
		end
	end
end
