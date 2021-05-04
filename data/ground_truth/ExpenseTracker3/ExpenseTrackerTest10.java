package com.kvannli.simonkvannli.dailybudget;


import android.support.test.espresso.DataInteraction;
import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static android.support.test.espresso.Espresso.onData;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.action.ViewActions.closeSoftKeyboard;
import static android.support.test.espresso.action.ViewActions.replaceText;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withClassName;
import static android.support.test.espresso.matcher.ViewMatchers.withContentDescription;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.anything;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class ExpenseTrackerTest10 {

    @Rule
    public ActivityTestRule<MainActivity> mActivityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Test
    public void expenseTrackerTest10() {
        ViewInteraction imageButton = onView(
                allOf(withContentDescription("Open navigation drawer"),
                        childAtPosition(
                                allOf(withId(R.id.action_bar),
                                        childAtPosition(
                                                withId(R.id.action_bar_container),
                                                0)),
                                0),
                        isDisplayed()));
        imageButton.perform(click());

        DataInteraction textView = onData(anything())
                .inAdapterView(allOf(withId(R.id.navigation_drawer),
                        childAtPosition(
                                withId(R.id.drawer_layout),
                                1)))
                .atPosition(2);
        textView.perform(click());

        ViewInteraction button = onView(
                allOf(withId(R.id.button2), withText("ADD INCOME"),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.LinearLayout")),
                                        2),
                                0),
                        isDisplayed()));
        button.perform(click());

        ViewInteraction textView2 = onView(
                allOf(withId(R.id.text), withText("Currently no income..."),
                        childAtPosition(
                                childAtPosition(
                                        IsInstanceOf.<View>instanceOf(android.widget.TableLayout.class),
                                        0),
                                0),
                        isDisplayed()));
        textView2.check(matches(withText("Currently no income...")));

        ViewInteraction editText = onView(
                allOf(withId(R.id.editText),
                        childAtPosition(
                                childAtPosition(
                                        withId(android.R.id.content),
                                        0),
                                0),
                        isDisplayed()));
        editText.perform(replaceText("uber"), closeSoftKeyboard());

        ViewInteraction button2 = onView(
                allOf(withId(R.id.button2), withText("ADD INCOME"),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.LinearLayout")),
                                        2),
                                0),
                        isDisplayed()));
        button2.perform(click());

        ViewInteraction tableRow = onView(
                allOf(childAtPosition(
                        childAtPosition(
                                IsInstanceOf.<View>instanceOf(android.widget.TableRow.class),
                                1),
                        0),
                        isDisplayed()));
        tableRow.check(matches(isDisplayed()));

        ViewInteraction editText2 = onView(
                allOf(withId(R.id.editText2),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.LinearLayout")),
                                        1),
                                0),
                        isDisplayed()));
        editText2.perform(replaceText("500"), closeSoftKeyboard());

        ViewInteraction button3 = onView(
                allOf(withId(R.id.button2), withText("ADD INCOME"),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.LinearLayout")),
                                        2),
                                0),
                        isDisplayed()));
        button3.perform(click());

        ViewInteraction tableRow2 = onView(
                allOf(childAtPosition(
                        childAtPosition(
                                IsInstanceOf.<View>instanceOf(android.widget.TableRow.class),
                                1),
                        0),
                        isDisplayed()));
        tableRow2.check(matches(isDisplayed()));

        ViewInteraction textView3 = onView(
                allOf(withId(R.id.text1), withText("500  MONTHLY"),
                        childAtPosition(
                                childAtPosition(
                                        IsInstanceOf.<View>instanceOf(android.widget.TableLayout.class),
                                        1),
                                0),
                        isDisplayed()));
        textView3.check(matches(withText("500  MONTHLY")));

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
