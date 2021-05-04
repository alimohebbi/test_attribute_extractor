package com.blogspot.e_kanivets.moneytracker.activity.record;


import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import com.blogspot.e_kanivets.moneytracker.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.*;
import static android.support.test.espresso.assertion.ViewAssertions.*;
import static android.support.test.espresso.matcher.ViewMatchers.*;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class ExpenseTrackerTest1 {

    @Rule
    public ActivityTestRule<MainActivity> mActivityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Test
    public void expenseTrackerTest1() {
        ViewInteraction appCompatButton = onView(
                allOf(withId(R.id.btn_add_income), withText("Add income"),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.LinearLayout")),
                                        1),
                                0),
                        isDisplayed()));
        appCompatButton.perform(click());

        ViewInteraction actionMenuItemView = onView(
                allOf(withId(R.id.action_done), withContentDescription("Add"),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.toolbar),
                                        2),
                                0),
                        isDisplayed()));
        actionMenuItemView.perform(click());

        ViewInteraction textView = onView(
                allOf(withId(R.id.textinput_error), withText("Field can't be empty."),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.til_price),
                                        1),
                                0),
                        isDisplayed()));
        textView.check(matches(withText("Field can't be empty.")));

        ViewInteraction appCompatEditText = onView(
                allOf(withId(R.id.et_price),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.til_price),
                                        0),
                                0),
                        isDisplayed()));
        appCompatEditText.perform(replaceText("1500"), closeSoftKeyboard());

        ViewInteraction actionMenuItemView2 = onView(
                allOf(withId(R.id.action_done), withContentDescription("Add"),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.toolbar),
                                        2),
                                0),
                        isDisplayed()));
        actionMenuItemView2.perform(click());

        ViewInteraction textView3 = onView(
                allOf(withId(R.id.textinput_error), withText("Field can't be empty."),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.til_category),
                                        1),
                                0),
                        isDisplayed()));
        textView3.check(matches(withText("Field can't be empty.")));

        ViewInteraction appCompatAutoCompleteTextView = onView(
                allOf(withId(R.id.et_title),
                        isDisplayed()));
        appCompatAutoCompleteTextView.perform(replaceText("GRA"), closeSoftKeyboard());

        ViewInteraction appCompatAutoCompleteTextView1 = onView(
                allOf(withId(R.id.et_category),
                        isDisplayed()));
        appCompatAutoCompleteTextView1.perform(replaceText("General"), closeSoftKeyboard());

        ViewInteraction actionMenuItemView3 = onView(
                allOf(withId(R.id.action_done), withContentDescription("Add"),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.toolbar),
                                        2),
                                0),
                        isDisplayed()));
        actionMenuItemView3.perform(click());

        ViewInteraction textView4 = onView(
                allOf(withId(R.id.tv_title), withText("GRA"),
                        childAtPosition(
                                childAtPosition(
                                        IsInstanceOf.<View>instanceOf(android.widget.LinearLayout.class),
                                        1),
                                0),
                        isDisplayed()));
        textView4.check(matches(withText("GRA")));

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
                        && view.equals(((ViewGroup) parent).getChildAt(position));
            }
        };
    }
}
