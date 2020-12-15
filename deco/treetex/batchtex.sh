for f in *[0-9]*tex; do echo $f; xelatex -halt-on-error "$f">/dev/null && echo "OK" && continue; echo "fail";  done
