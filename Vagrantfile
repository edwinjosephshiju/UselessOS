Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vm.hostname = "uselessos"

  # GUI and VM config
  config.vm.provider "virtualbox" do |vb|
    vb.name = "UselessOS"
    vb.gui = true
    vb.memory = "2048"
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--vram", "128"]
    vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
    vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
    vb.customize ["modifyvm", :id, "--audiocontroller", "ac97"]
    vb.customize ["modifyvm", :id, "--audioout", "on"]
    vb.customize ["modifyvm", :id, "--paravirtprovider", "kvm"]
    vb.customize ["modifyvm", :id, "--nestedpaging", "on"]
    vb.customize ["modifyvm", :id, "--largepages", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  # Map the apps folder so the provisioning script can copy it
  config.vm.synced_folder "./apps", "/vagrant/apps", type: "rsync"
  config.vm.synced_folder "./scripts", "/vagrant/scripts", type: "rsync"

  # Provisioning
  config.vm.provision "shell", inline: "bash /vagrant/scripts/01-install-core.sh"
  config.vm.provision "shell", inline: "bash /vagrant/scripts/02-configure-system.sh"
  config.vm.provision "shell", inline: "bash /vagrant/scripts/03-deploy-apps.sh"
  config.vm.provision "shell", inline: "bash /vagrant/scripts/04-setup-qwen.sh"
end
