// @copyright (C) 2023 Robert Bosch GmbH.
//// The reproduction, distribution and utilization of this file as well as the communication of its contents to others
// without express authorization is prohibited. Offenders will be held liable for the payment of damages. All rights
// reserved in the event of the grant of a patent, utility model or design.
//
// @file ulrr_gtest_entry.cpp
// @author Thomas Badura (XC-AD/ERA2)

#include "gtest/gtest.h"

int main(int argc, char** argv)
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
