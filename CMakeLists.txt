cmake_minimum_required(VERSION 3.5)

project(coco)

set(TARGET_NAME HoCo)

find_program(COCO "coco")

set(generated_source_files
        ${generated_source_files}/main.py
)

set(GRAMMAR_FILE ../parser_src/grammar.atg.py)

add_custom_command(
        OUTPUT ${generated_source_files}
        COMMAND ${COCO} -c ${GRAMMAR_FILE}
)

add_custom_target(
        always_run_target ALL
        DEPENDS ${generated_source_files}
)






