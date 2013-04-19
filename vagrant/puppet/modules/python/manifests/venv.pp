class python::venv($ensure=present, $owner=undef, $group=undef) inherits python::dev {

  package { "python-virtualenv":
    ensure => $ensure,
  }
}
