cmake_minimum_required(VERSION 3.16)
project(ComputeJacobianFromDisplacement)

find_package(ITK REQUIRED)

include(${ITK_USE_FILE})

add_executable(itk_compute_jacobian itk_compute_jacobian.cxx)
target_link_libraries(itk_compute_jacobian PRIVATE ${ITK_LIBRARIES})
target_include_directories(itk_compute_jacobian PRIVATE ${ITK_INCLUDE_DIRS})

