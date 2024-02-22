cmake_minimum_required(VERSION 3.5)

project(coco)

set(COCO_FRAME_DIR ../coco_exec)
find_program(COCO ${COCO_FRAME_DIR}/Coco.exe  HINTS .. )


set(PARSER_DIR_SRC ../parser_src)
add_custom_target(build-time-make-directory ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory ${PARSER_DIR_SRC})


set(generated_source_files
        ${PARSER_DIR_SRC}/Scanner.cpp
        ${PARSER_DIR_SRC}/Scanner.h
        ${PARSER_DIR_SRC}/Parser.cpp
        ${PARSER_DIR_SRC}/Parser.h
)
set_source_files_properties(${generated_source_files} PROPERTIES GENERATED TRUE)

set(GRAMMAR_FILE ../grammar.atg)

add_custom_command(
        OUTPUT ${generated_source_files}
        COMMAND ${COCO} ${GRAMMAR_FILE} -frames ${COCO_FRAME_DIR} -o ${PARSER_DIR_SRC}
        COMMENT "Generating Parser from ${GRAMMAR_FILE} with ${COCO}"
)

set(SOURCES 
    main.cpp
    ${generated_source_files}
)

add_executable(${PROJECT_NAME} ${SOURCES})







