class python::dev($ensure=present, $version=latest) {

  $python = $version ? {
    'latest' => "python",
    default => "python${version}",
  }

  # python development packages depends on the correct python package:
  $package_suffix = $operatingsystem ? {
    /(?i)centos|fedora|redhat/ => 'devel',
    default                    => 'dev',
  }

  package { "${python}-${package_suffix}":
    ensure => $ensure,
  }
}
