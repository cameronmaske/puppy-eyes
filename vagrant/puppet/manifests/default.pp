Exec {
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

#Apt get update if older than a week!
exec { 'apt-get update':
    command => "/usr/bin/apt-get update && apt-get install -y libjpeg8 libjpeg8-dev libjpeg62-dev libfreetype6 libfreetype6-dev libpq-dev pep8 libevent-dev libgraphviz-dev libxslt1.1 libxslt1-dev python-libxslt1",
    onlyif => "/bin/bash -c 'exit $(( $(( $(date +%s) - $(stat -c %Y /var/lib/apt/lists/$( ls /var/lib/apt/lists/ -tr1|tail -1 )) )) <= 604800 ))'"
}

#Python
class { "python::dev":
    version => "2.7"
}

include python::dev

#Redis.
include redis::dependencies
package { $redis::dependencies::packages:
  ensure => present,
}
include redis::server


python::venv::isolate { "/home/virtual-env/":
    version => "2.7",
    requirements => "/home/vagrant/puppy-eyes/requirements.txt",

}


include python::venv

#Based on http://projects.puppetlabs.com/projects/1/wiki/simple_text_patterns
define line($file, $line, $ensure = 'present') {
    case $ensure {
        default : { err ( "unknown ensure value ${ensure}" ) }
        present: {
            exec { "/bin/echo '${line}' >> '${file}'":
                unless => "/bin/grep -qFx '${line}' '${file}'"
            }
        }
        absent: {
            exec { "/bin/grep -vFx '${line}' '${file}' | /usr/bin/tee '${file}' > /dev/null 2>&1":
              onlyif => "/bin/grep -qFx '${line}' '${file}'"
            }

            # Use this resource instead if your platform's grep doesn't support -vFx;
            # note that this command has been known to have problems with lines containing quotes.
            # exec { "/usr/bin/perl -ni -e 'print unless /^\\Q${line}\\E\$/' '${file}'":
            #     onlyif => "/bin/grep -qFx '${line}' '${file}'"
            # }
        }
    }
}

class venv_setup {
    line {"append_bashrc" :
        line => "source /home/virtual-env/bin/activate",
        file => '/home/vagrant/.bashrc',
    }
}

class heroku_toolbelt {
    # Install heroku toolbelt
    exec { "install_toolbelt":
        command => "wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh",
        creates => "/usr/local/heroku"
    }
}

include heroku_toolbelt


class cleanup {
    exec { "remove_old":
        command => "rm -f /home/vagrant/postinstall.sh",
    }
}

include cleanup
