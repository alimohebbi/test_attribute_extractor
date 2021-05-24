package com.blogspot.e_kanivets.moneytracker.activity.record;


import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import static android.support.test.InstrumentationRegistry.getInstrumentation;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.Espresso.pressBack;
import static android.support.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu;
import static android.support.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition;
import static android.support.test.espresso.action.ViewActions.*;
import static android.support.test.espresso.assertion.ViewAssertions.*;
import static android.support.test.espresso.matcher.ViewMatchers.*;

import com.blogspot.e_kanivets.moneytracker.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class AppTestMigrator_expenseTrackerTest10_3 {

    @Rule
    public ActivityTestRule<com.blogspot.e_kanivets.moneytracker.activity.record.MainActivity> mActivityTestRule = new ActivityTestRule<>(com.blogspot.e_kanivets.moneytracker.activity.record.MainActivity.class);

    @Test
    public void apptestmigrator_expensetrackertest10_3() {
        onView(withContentDescription("Open navigation drawer")).perform(click());
        
        pressBack();
        
        onView(withText("Week")).perform(click());
        
        onView(withText("Day")).perform(click());
        
        onView(withId(R.id.btn_add_income)).perform(click());
        
        onView(withId(R.id.et_title)).perform(replaceText("uber"), closeSoftKeyboard());
        
        onView(withContentDescription("Navigate up")).perform(click());
        
        onView(withId(R.id.tv_period)).check(matches(isDisplayed()));
        
        onView(withContentDescription("Open navigation drawer")).perform(click());
        
        pressBack();
        
        onView(withId(R.id.btn_add_income)).perform(click());
        
        onView(withId(R.id.et_title)).perform(replaceText("500"), closeSoftKeyboard());
        
        onView(withContentDescription("Navigate up")).perform(click());
        
        onView(withId(R.id.tv_period)).check(matches(isDisplayed()));
        
        onView(withId(R.id.tv_period)).check(matches(withText("18 Apr, 2021")));
        
        }

        private static Matcher<View> childAtPosition(
            final Matcher<View> parentMatcher, final int position) {

        return new TypeSafeMatcher<View>() {
            @Override
            public void describeTo(Description description) {
                description.appendText("Child at position " + position + " in parent ");
                parentMatcher.describeTo(description);
            }

            @Override
            public boolean matchesSafely(View view) {
                ViewParent parent = view.getParent();
                return parent instanceof ViewGroup && parentMatcher.matches(parent)
                        && view.equals(((ViewGroup)parent).getChildAt(position));
            }
        };
    }
    }
