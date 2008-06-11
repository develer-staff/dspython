def f():
  import sys
  print "Cleared importer cache.."
  if sys.path_importer_cache.has_key("cf0:/python/lib/python24.zip"):
    del sys.path_importer_cache["cf0:/python/lib/python24.zip"]
  try:
    import site
  except SyntaxError:
    pass
