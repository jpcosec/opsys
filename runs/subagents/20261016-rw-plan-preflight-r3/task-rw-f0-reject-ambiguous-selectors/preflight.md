<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="bash">
<｜｜DSML｜｜ parameter name="command" string="true">cd /home/jp/proyectos/SLDB_1/deskops && sed -n 2595,2660p deskops/operations.py && echo ---- && sed -n 2730,2760p deskops/operations.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
<｜｜DSML｜｜ invoke name="bash">
<｜｜DSML｜｜ parameter name="command" string="true">cd /home/jp/proyectos/SLDB_1/deskops && sed -n 370,395p deskops/cli/main.py && echo ---- && grep -n "_make_repo\|^def _cli\|def _cli" tests/test_lifecycle_end_to_end.py | head -20</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
