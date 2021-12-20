#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# This file is formatted with Python Black
#

import ratbag

import pytest


def test_resolution():
    device = ratbag.Device(object(), "test device", "nopath")
    profile = ratbag.Profile(device, 0)

    # invalid index
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, -1, (0, 0))

    # negative dp
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, (-1, -1))

    # dpi not an int
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, ("asbc", 1))

    # dpi not a 2-value tuple
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, (1, 2, 3))

    # dpi list negative
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, (1, 2), dpi_list=[-1])

    # dpi list not a list
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, (1, 2), dpi_list=-1)

    # capability not in the enum
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, (1, 2, 3), capabilities=[1])

    # default values
    r = ratbag.Resolution(profile, 0, (200, 200))
    assert r.capabilities == []
    assert not r.active
    assert not r.default
    assert r.enabled
    # correctly added to the profile?
    assert r in profile.resolutions.values()
    assert r.index in profile.resolutions
    assert r.dpi == (200, 200)

    # duplicate index
    with pytest.raises(AssertionError):
        ratbag.Resolution(profile, 0, (200, 200))

    # caps assigned properly?
    r = ratbag.Resolution(
        profile,
        1,
        (200, 200),
        capabilities=[ratbag.Resolution.Capability.SEPARATE_XY_RESOLUTION],
    )
    assert r.capabilities == [ratbag.Resolution.Capability.SEPARATE_XY_RESOLUTION]


def test_resolution_set_default():
    device = ratbag.Device(object(), "test device", "nopath")
    for i in range(5):
        profile = ratbag.Profile(device, i)
        for j in range(5):
            ratbag.Resolution(profile, j, (j * 100, j * 100))

    r11 = device.profiles[1].resolutions[1]
    r13 = device.profiles[1].resolutions[3]
    r22 = device.profiles[2].resolutions[2]
    r24 = device.profiles[2].resolutions[4]
    # we start with no default resolution
    assert [r.default for r in device.profiles[1].resolutions.values()].count(True) == 0

    r13.set_default()
    assert r13.default
    assert r13.dirty
    assert [r.default for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 1
    r11.set_default()
    assert r11.default
    assert r11.dirty
    assert not r13.default
    assert r13.dirty
    assert [r.default for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 2
    # different profile, shouldn't affect r11/r13
    r22.set_default()
    assert r22.default
    assert r22.dirty
    assert r11.default
    assert r11.dirty
    assert not r13.default
    assert r13.dirty
    assert [r.default for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 2
    assert [r.default for r in device.profiles[2].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[2].resolutions.values()].count(True) == 1
    r24.set_default()
    assert r24.default
    assert r24.dirty
    assert not r22.default
    assert r22.dirty
    assert r11.default
    assert r11.dirty
    assert not r13.default
    assert r13.dirty
    assert [r.default for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 2
    assert [r.default for r in device.profiles[2].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[2].resolutions.values()].count(True) == 2


def test_resolution_set_active():
    device = ratbag.Device(object(), "test device", "nopath")
    for i in range(5):
        profile = ratbag.Profile(device, i)
        for j in range(5):
            ratbag.Resolution(profile, j, (j * 100, j * 100))

    r11 = device.profiles[1].resolutions[1]
    r13 = device.profiles[1].resolutions[3]
    r22 = device.profiles[2].resolutions[2]
    r24 = device.profiles[2].resolutions[4]
    # we start with no active resolution
    assert [r.active for r in device.profiles[1].resolutions.values()].count(True) == 0

    r13.set_active()
    assert r13.active
    assert r13.dirty
    assert [r.active for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 1
    r11.set_active()
    assert r11.active
    assert r11.dirty
    assert not r13.active
    assert r13.dirty
    assert [r.active for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 2
    # different profile, shouldn't affect r11/r13
    r22.set_active()
    assert r22.active
    assert r22.dirty
    assert r11.active
    assert r11.dirty
    assert not r13.active
    assert r13.dirty
    assert [r.active for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 2
    assert [r.active for r in device.profiles[2].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[2].resolutions.values()].count(True) == 1
    r24.set_active()
    assert r24.active
    assert r24.dirty
    assert not r22.active
    assert r22.dirty
    assert r11.active
    assert r11.dirty
    assert not r13.active
    assert r13.dirty
    assert [r.active for r in device.profiles[1].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[1].resolutions.values()].count(True) == 2
    assert [r.active for r in device.profiles[2].resolutions.values()].count(True) == 1
    assert [r.dirty for r in device.profiles[2].resolutions.values()].count(True) == 2


def test_profile_set_active():
    device = ratbag.Device(object(), "test device", "nopath")
    for i in range(5):
        ratbag.Profile(device, i)

    p1 = device.profiles[1]
    p3 = device.profiles[3]

    # None are active by default
    assert [p.active for p in device.profiles.values()].count(True) == 0

    p1.set_active()
    assert p1.active
    assert p1.dirty
    assert [p.active for p in device.profiles.values()].count(True) == 1
    assert [p.dirty for p in device.profiles.values()].count(True) == 1

    p3.set_active()
    assert not p1.active
    assert p1.dirty
    assert p3.active
    assert p3.dirty
    assert [p.active for p in device.profiles.values()].count(True) == 1
    assert [p.dirty for p in device.profiles.values()].count(True) == 2


def test_profile_set_enabled():
    device = ratbag.Device(object(), "test device", "nopath")
    for i in range(5):
        ratbag.Profile(device, i)

    p1 = device.profiles[1]
    p3 = device.profiles[3]

    # All are enabled by default
    assert [p.enabled for p in device.profiles.values()].count(False) == 0

    p1.enabled = False
    assert not p1.enabled
    assert p1.dirty
    assert [p.enabled for p in device.profiles.values()].count(False) == 1
    assert [p.dirty for p in device.profiles.values()].count(True) == 1

    p3.enabled = False
    assert not p3.enabled
    assert p3.dirty
    assert [p.enabled for p in device.profiles.values()].count(False) == 2
    assert [p.dirty for p in device.profiles.values()].count(True) == 2


def test_profile_set_default():
    device = ratbag.Device(object(), "test device", "nopath")
    for i in range(5):
        ratbag.Profile(device, i, capabilities=[ratbag.Profile.Capability.SET_DEFAULT])

    p1 = device.profiles[1]
    p3 = device.profiles[3]

    # None are active by default
    assert [p.default for p in device.profiles.values()].count(True) == 0

    p1.set_default()
    assert p1.default
    assert p1.dirty
    assert [p.default for p in device.profiles.values()].count(True) == 1
    assert [p.dirty for p in device.profiles.values()].count(True) == 1

    p3.set_default()
    assert not p1.default
    assert p1.dirty
    assert p3.default
    assert p3.dirty
    assert [p.default for p in device.profiles.values()].count(True) == 1
    assert [p.dirty for p in device.profiles.values()].count(True) == 2
