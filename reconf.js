cfg = rs.conf();
cfg.members[0].host = "10.2.0.1:27017";
rs.reconfig(cfg);
rs.status();
