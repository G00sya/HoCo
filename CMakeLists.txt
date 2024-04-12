cmake_minimum_required(VERSION 3.5)

project(coco)

set(TARGET_NAME HoCo)

find_program(COCO "coco")
find_program(Python "python")

set(generated_source_files ../parser_src/VeKrestKrest)

set(OUTFILES ../out.txt)

set(GRAMMAR_FILE ../parser_src/grammar.atg)

add_custom_command(
        OUTPUT ${generated_source_files}
        COMMAND ${COCO} -c ${GRAMMAR_FILE}
        COMMENT "Generating Parser from ${GRAMMAR_FILE} with ${COCO}"
)

set(EXECUTABLE ../example.txt)

add_custom_command(
        OUTPUT ${OUTFILES}
        DEPENDS ${generated_source_files}
        COMMAND ${Python}  ../parser_src/VeKrestKrest.py ${EXECUTABLE}
        COMMENT "Launching ${generated_source_files} ${EXECUTABLE} with ${Python}"
)

add_custom_target(
        always_run_target ALL
        DEPENDS ${generated_source_files} ${OUTFILES}
)
